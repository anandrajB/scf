from django.contrib import admin
from django.urls import path , include
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='SCF API DOCUMENTATION')

# -----------------------------------------------------------------------------

# URL FOR NON-TENANT ( ALIAS ADMIN : SCF ) - PUBLIC SCHEMA

# -----------------------------------------------------------------------------

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/',include('accounts.urls')),
    path('api/',include('transaction.urls')),
    path('apidoc/', schema_view)
]
