from django.contrib import admin


from .models import Invoices, Programs, invoice_uploads, workevents, workflowitems 
# Register your models here.
admin.site.register(Programs)
admin.site.register(workevents)
admin.site.register(workflowitems)
admin.site.register(invoice_uploads)
admin.site.register(Invoices)