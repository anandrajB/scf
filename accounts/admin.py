from django.contrib import admin
from django import forms
from django.forms import Textarea
from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy
from .models import Banks, Countries, Currencies, PhoneOTP, User , Parties, signatures, userprocessauth




class MyAdminSite(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = ugettext_lazy('My site admin')

    # Text to put in each page's <h1> (and above login form).
    site_header = ugettext_lazy('SCF ADMIN PANEL')

    # Text to put at the top of the admin index page.
    index_title = ugettext_lazy('Site administration')


admin_site = MyAdminSite()



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'phone', 'first_name','last_name','display_name')}),
        ('Permissions', {'fields': ('is_active', 'is_maker', 'is_sign_a','is_sign_b','is_supervisor', 
                                    'is_administrator',  'user_permissions')}),
        ('Important Dates', {'fields': ('last_login',)}),
    )
    filter_horizontal = (
        'user_permissions',
    )

    list_display = ('email', 'phone', 'is_supervisor', "is_administrator" ,'is_active')
    # list_filter = ('is_supervisor','is_administrator','created_date','is_active')



admin.site.register(Parties)
admin.site.register(Banks)
admin.site.register(Currencies)
admin.site.register(Countries)
admin.site.register(userprocessauth)
admin.site.register(signatures)