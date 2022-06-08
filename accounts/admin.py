from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy
from .models import (
    Banks, 
    Countries, 
    Currencies, 
    Models, 
    User ,
    Parties,
    signatures,
    userprocessauth ,
    Action
)

from rest_framework.authtoken.models import Token 
from django.utils.safestring import mark_safe




class MyAdminSite(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = ugettext_lazy('FINFLO')

    # Text to put in each page's <h1> (and above login form).
    site_header = ugettext_lazy('FINFLO ADMIN PANEL')

    # Text to put at the top of the admin index page.
    index_title = ugettext_lazy('Finflo administration panel')


admin_site = MyAdminSite()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    

    

    fieldsets = (
        (None, {'fields': ('email', 'phone', 'first_name','last_name','display_name')}),
        ('profile picture', {'fields': ('profile_tags',)}),
        ('Permissions', {'fields': ('is_active','is_supervisor', 'is_administrator',)}),
        ('Party', {'fields': ('party',)}),
        ('Important Dates', {'fields': ('last_login',)}),
    )
    filter_horizontal = (
        'user_permissions',
    )
    readonly_fields = ['profile_tags']
    list_display = ('email', 'phone', 'party','is_supervisor', "is_administrator" ,'is_active')
    search_fields = ['email','phone','party__name']
    # list_filter = ('is_supervisor','is_administrator','is_active')



admin.site.register(Parties)
admin.site.register(Banks)
admin.site.register(Currencies)
admin.site.register(Countries)
admin.site.register(userprocessauth)
admin.site.register(Action)
admin.site.register(Models)
admin.site.register(signatures)
# admin.site.unregister(Token)
admin.site.unregister(Group)


