from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib import admin
from django.utils.translation import ugettext as _
from django.utils.encoding import force_text
from django import forms

from users.models import User, Membership, Profile, Address

import import_export

import logging
log = logging.getLogger(__name__)


class MembershipInline(admin.StackedInline):
    model = Membership
    extra = 0


class AddressInline(admin.StackedInline):
    model = Address
    extra = 0


class UserResource(import_export.resources.ModelResource):
    class Meta:
        model = User


class MembershipResource(import_export.resources.ModelResource):
    class Meta:
        model = Membership


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password confirmation'), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', )
        exclude = ('username', )

    def is_valid(self):
        log.info(force_text(self.errors))
        return super(UserCreationForm, self).is_valid()

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label=_("Password"))

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial.get("password")