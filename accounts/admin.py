from django.contrib import admin
from django import forms
from django.contrib import admin
from django.forms import Textarea
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin 
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.db import models
from .models import Banks, Countries, Currencies, User , Parties, customer, workevents, workflowitems


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("email", "username","phone")

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ("email", "phone", "username","password", "is_active", "is_superuser","is_staff")

    def clean_password(self):
        return self.initial["password"]


# class UserAdmin(BaseUserAdmin):
#     # The forms to add and change user instances
#     form = UserChangeForm
#     add_form = UserCreationForm

#     # The fields to be used in displaying the User model.
#     # These override the definitions on the base UserAdmin
#     # that reference specific fields on auth.User.
#     list_display = ("email", "phone", "is_admin")
#     list_filter = ("is_admin",)
#     fieldsets = (
#         (None, {"fields": ("email", "password")}),
#         ("Personal info", {"fields": ("phone","is_company")}),
#         ("Permissions", {"fields": ("is_active", "is_admin","is_staff","is_superuser",)}),
#         ("others", {"fields": ("groups", "user_permissions")}),
#     )
#     # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
#     # overrides get_fieldsets to use this attribute when creating a user.
#     add_fieldsets = (
#         (
#             None,
#             {
#                 "classes": ("wide",),
#                 "fields": ("email", "phone", "password1", "password2"),
#             },
#         ),
#     )
#     search_fields = ("email",)
#     ordering = ("email",)
#     filter_horizontal = ()

class UserAdminConfig(UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm

    model = User
    search_fields = ('phone', 'email', 'password')
    list_filter = ('phone',)
    ordering = ('-is_staff',)
    list_display = ('email',"username","is_staff","is_superuser")
    fieldsets = (
        (None, {'fields': ('phone', 'username','email','password',)}),
        ('Permissions', {'fields': ( 'is_superuser',"is_staff",'is_active','groups','user_permissions')}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'email', 'password', 'is_active', 'is_staff',  'is_superuser')}
         ),
    )




# Now register the new UserAdmin...
admin.site.register(User, UserAdminConfig)

admin.site.register(workflowitems)
admin.site.register(workevents)
admin.site.register(Parties)
admin.site.register(customer)
admin.site.register(Banks)
admin.site.register(Currencies)
admin.site.register(Countries)