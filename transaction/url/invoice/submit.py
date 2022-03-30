from django.urls import path
from django.urls.conf import include
from accounts.views import index
from transaction.api.InvoiceTransition import (
    InvoiceSubmitSign_ATransitionApi,
    InvoiceSubmitSign_BTransitionApi,
    InvoiceSubmitSign_CTransitionApi
)

# SUBMIT  - SIGNATURE LEVELS


urlpatterns = [
    path('sign_a/<int:pk>/',InvoiceSubmitSign_ATransitionApi.as_view()),
    path('sign_b/<int:pk>/',InvoiceSubmitSign_BTransitionApi.as_view()),
    path('sign_c/<int:pk>/',InvoiceSubmitSign_CTransitionApi.as_view())
]

