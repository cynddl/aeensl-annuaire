from django.contrib.sites.models import Site
from django.contrib import admin

from users.models import User, Profile, Membership


class MembershipInline(admin.StackedInline):
    model = Membership
    extra = 0


class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', )
    list_filter = ('is_admin', )

    inlines = (ProfileInline, )


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'first_year', 'field')
    search_fields = ('first_name', 'last_name')


class MembershipAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'uid', 'status', 'created_on', 'start_date')
    list_filter = ('status', 'membership_type')
    list_editable = ('status', )
    search_fields = ('user__email', 'user__profile__first_name', 'user__profile__last_name', 'uid')

    fieldsets = [
        (None, {
            'fields': ['user', 'status', 'created_on', 'start_date',
                       'duration', 'in_couple', 'partner_name',
                       'membership_type']
        }),
        ('Paiement', {
            'fields': ['amount', 'payment_amount', 'payment_date',
                       'payment_type', 'payment_bank', 'payment_reference',
                       'payment_first_name', 'payment_last_name']
        })
    ]
    readonly_fields = ('created_on', )

    def utilisateur(self, obj):
        return obj.user.profile


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.unregister(Site)
