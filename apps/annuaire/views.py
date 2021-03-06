from django.views.generic import TemplateView, DetailView, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models.aggregates import Count

import django_filters
import django_tables2 as tables

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

from users.models import Profile
from . import filters


@method_decorator(login_required, name='dispatch')
class AnnuaireView(TemplateView):
    template_name = "annuaire/index.html"


@method_decorator(login_required, name='dispatch')
class PromoListView(TemplateView):
    template_name = "annuaire/promo_list.html"

    def get_context_data(self, **kwargs):
        query = Profile.objects.values('entrance_year').order_by('entrance_year').annotate(Count('entrance_year'))
        counts = {
            c['entrance_year']: c['entrance_year__count']
            for c in query if c['entrance_year'] is not None
        }

        context = super(PromoListView, self).get_context_data(**kwargs)
        context['counts_promo'] = sorted(counts.items(), reverse=True)
        return context


@method_decorator(login_required, name='dispatch')
class ProfileDetailView(DetailView):
    template_name = "annuaire/profile_detail.html"
    queryset = Profile.objects.all()

    def is_current_user(self):
        return self.get_object() == self.request.user.profile


@method_decorator(login_required, name='dispatch')
class CurrentProfileDetailView(ProfileDetailView):
    def get_object(self):
        return self.request.user.profile


@method_decorator(login_required, name='dispatch')
class ProfileMembershipView(DetailView):
    template_name = "annuaire/profile_membership_detail.html"
    queryset = Profile.objects.all()

    def is_current_user(self):
        return self.get_object() == self.request.user.profile


@method_decorator(login_required, name='dispatch')
class CurrentProfileMembershipView(ProfileMembershipView):
    def get_object(self):
        return self.request.user.profile

# Table views & utils
# -------------------

class ProfileTable(tables.Table):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'entrance_school',
                  'entrance_year', 'entrance_field')

    first_name = tables.LinkColumn("annuaire:user_profile", args=[tables.utils.A('pk')], verbose_name="Prénom")
    last_name = tables.LinkColumn("annuaire:user_profile", args=[tables.utils.A('pk')], verbose_name="Nom")
    entrance_school = tables.Column(verbose_name="École")
    entrance_year = tables.Column(verbose_name="Année d'entrée")
    entrance_field = tables.Column(verbose_name="Discipline d'entrée")


class PagedFilteredTableView(tables.SingleTableView):
    filter_class = None
    formhelper_class = None
    context_filter_name = 'filter'

    def get_queryset(self, **kwargs):
        qs = super(PagedFilteredTableView, self).get_queryset()
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        self.filter.form.helper = self.formhelper_class()
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super(PagedFilteredTableView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        return context


@method_decorator(login_required, name='dispatch')
class ProfileListView(PagedFilteredTableView):
    template_name = "annuaire/profile_list.html"
    paginate_by = 25
    model = Profile

    table_class = ProfileTable
    filter_class = filters.ProfileListFilter
    formhelper_class = filters.ProfileListFormHelper

    def post(self, request, *args, **kwargs):
        return PagedFilteredTableView.as_view()(request)


@method_decorator(login_required, name='dispatch')
class ProfilePromotionListView(ProfileListView):
    def get_queryset(self, **kwargs):
        qs = super(ProfileListView, self).get_queryset(**kwargs)
        qs = qs.filter(entrance_year=self.kwargs['year'])
        return qs


@method_decorator(login_required, name='dispatch')
class ProfileSearchView(ProfileListView):
    template_name = "annuaire/profile_search.html"

    filter_class = filters.SearchFilter
    formhelper_class = filters.SearchFormHelper


@method_decorator(login_required, name='dispatch')
class HonoraryProfileListView(ListView):
    template_name = "annuaire/membres_honoraires.html"
    model = Profile
    queryset = Profile.objects.filter(is_honorary=True).order_by('last_name', 'first_name')
