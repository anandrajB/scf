from django.contrib import admin

from .models import Invoices, invoice_uploads
admin.site.register(invoice_uploads)
admin.site.register(Invoices)