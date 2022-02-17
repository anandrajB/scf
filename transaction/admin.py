from django.contrib import admin


from .models import Invoices, Programs, Invoiceuploads, workevents, workflowitems 
# Register your models here.
admin.site.register(Programs)
admin.site.register(workevents)
admin.site.register(workflowitems)
admin.site.register(Invoiceuploads)
admin.site.register(Invoices)