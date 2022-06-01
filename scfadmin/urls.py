from django import urls
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from rest_framework_swagger.views import get_swagger_view
from accounts.views import index , endpoint
from django.conf import settings
from django.conf.urls.static import static

# swageer url
schema_view = get_swagger_view(title='SCF API DOCUMENTATION')


urlpatterns = [
    path('',index,name='home-page'),
    path('api-urls/',endpoint ,name = 'api-end-points'),
    path('admin/', admin.site.urls,),
    path('rest-auth-client/',include('rest_framework.urls')),
    path('api-auth/',include('accounts.urls')),
    path('api/',include('transaction.urls')),
    path('apidoc/', schema_view),
    path('__debug__/', include('debug_toolbar.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# custom pages for 404 and 500 error

handler404 = 'accounts.views.error_404_view'
handler500 = 'accounts.views.error_500_view'
