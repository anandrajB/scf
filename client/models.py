from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

class Client(TenantMixin):
    Org_Name = models.CharField(max_length=255) 
    City= models.CharField(max_length=255)
    State= models.CharField(max_length=255)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

class Domain(DomainMixin):
    pass
