from django.contrib import admin

from transaction.models import Programs, workevents
# Register your models here.
admin.site.register(Programs)
admin.site.register(workevents)
