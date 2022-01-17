from django.contrib import admin


from .models import Programs, workevents 
# Register your models here.
admin.site.register(Programs)
admin.site.register(workevents)