from django.urls import path
from django.urls.conf import include
from accounts.views import index
from transaction.api.InvoiceTransition import (
    InvoiceApproveSign_ATransitionApiView,
    InvoiceApproveSign_BTransitionApiView,
    InvoiceApproveSign_CTransitionApiView
)

# APPROVE URLS


urlpatterns = [
    path('sign_a/<int:pk>/',InvoiceApproveSign_ATransitionApiView.as_view()),
    path('sign_b/<int:pk>/',InvoiceApproveSign_BTransitionApiView.as_view()),
    path('sign_c/<int:pk>/',InvoiceApproveSign_CTransitionApiView.as_view())
]

