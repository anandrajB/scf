from django.contrib import admin
from django.urls import path , include
from accounts.views import index ,endpoint
from rest_framework_swagger.views import get_swagger_view
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_swagger_view(title='SCF API DOCUMENTATION')


# –––––––––––––––––––––––––––––––––––––––––#
#        PUBLIC URL'S  (non-tenant)        #
# –––––––––––––––––––––––––––––––––––––––––#


urlpatterns = [
    path('',index,name='home-page'),
    path('admin/', admin.site.urls,),
    path('rest-auth-client/',include('rest_framework.urls')),
    path('api-auth/',include('accounts.urls')),
    path('api/',include('transaction.urls')),
    path('api-urls/',endpoint ,name = 'api-end-points'),
    path('apidoc/', schema_view),
    
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler for 404 pages in production 

handler404 = 'accounts.views.error_404_view'
handler500 = 'accounts.views.error_500_view'
