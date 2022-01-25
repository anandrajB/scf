from django.contrib import admin
from .models import Client , Domain

# Register your models here.
admin.site.register(Client)
admin.site.register(Domain)