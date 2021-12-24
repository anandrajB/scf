from django.contrib import admin

from .models import Programs , Invoices, invoice_uploads
admin.site.register(invoice_uploads)
admin.site.register(Invoices)