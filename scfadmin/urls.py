from django import urls
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from rest_framework_swagger.views import get_swagger_view
from accounts.views import index

schema_view = get_swagger_view(title='SCF API DOCUMENTATION')


urlpatterns = [
    path('',index,name='home-page'),
    path('admin/', admin.site.urls,),
    path('rest-auth-client/',include('rest_framework.urls')),
    path('api-auth/',include('accounts.urls')),
    path('api/',include('transaction.urls')),
    path('apidoc/', schema_view),
    path('__debug__/', include('debug_toolbar.urls')),
    path('silk/', include('silk.urls', namespace='silk'))

    
]

# handler for 404 pages in production 

handler404 = 'accounts.views.error_404_view'
