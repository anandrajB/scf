from django.contrib import admin


from .models import FundingRequest, InterestChoice, InterestRateType, Invoices, Pairings, Programs, Invoiceuploads, workevents, workflowitems
# Register your models here.
admin.site.register(Programs)
admin.site.register(InterestChoice)
admin.site.register(InterestRateType)
admin.site.register(workevents)
admin.site.register(workflowitems)
admin.site.register(Invoiceuploads)
admin.site.register(Invoices)
admin.site.register(Pairings)
admin.site.register(FundingRequest)
