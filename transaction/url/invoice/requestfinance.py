from django.urls import path
from django.urls.conf import include
from accounts.views import index
from transaction.api.InvoiceTransition import (
    REQ_FIN_SignA_APF,
    REQ_FIN_SignB_APF,
    REQ_FIN_SignC_APF
)

# RF URLS


urlpatterns = [
    path('sign_a/<int:pk>/',REQ_FIN_SignA_APF.as_view()),
    path('sign_b/<int:pk>/',REQ_FIN_SignB_APF.as_view()),
    path('sign_c/<int:pk>/',REQ_FIN_SignC_APF.as_view())
]

