from django.urls import path
from django.urls.conf import include
from accounts.views import index
from transaction.api.InvoiceTransition import (
    InvoiceRejectSign_ATransitionApiView,
    InvoiceRejectSign_BTransitionApiView,
    InvoiceRejectSign_CTransitionApiView
)

# REJECT


urlpatterns = [
    path('sign_a/<int:pk>/',InvoiceRejectSign_ATransitionApiView.as_view()),
    path('sign_b/<int:pk>/',InvoiceRejectSign_BTransitionApiView.as_view()),
    path('sign_c/<int:pk>/',InvoiceRejectSign_CTransitionApiView.as_view())
]

