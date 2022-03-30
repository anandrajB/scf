from django.contrib import admin
from django.urls import path , include
from accounts.views import index
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='SCF API DOCUMENTATION')


# –––––––––––––––––––––––––––––––––––––––––
#        PUBLIC URL'S  (non-tenant)   
# –––––––––––––––––––––––––––––––––––––––––


urlpatterns = [
    path('',index,name='home-page'),
    path('admin/', admin.site.urls,),
    path('rest-auth-client/',include('rest_framework.urls')),
    path('api-auth/',include('accounts.urls')),
    path('api/',include('transaction.urls')),
    path('apidoc/', schema_view),
    
]

# handler for 404 pages in production 

handler404 = 'accounts.views.error_404_view'
