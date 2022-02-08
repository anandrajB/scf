from django.contrib import admin


from .models import Programs, submodels, workevents, workflowitems 
# Register your models here.
admin.site.register(Programs)
admin.site.register(workevents)
admin.site.register(workflowitems)
admin.site.register(submodels)