from django.urls import path
from django.urls.conf import include
from accounts.views import index
from transaction.api.InvoiceTransition import (
    RejectSign_AApiview_APF,
    RejectSign_BApiview_APF,
    RejectSign_CApiview_APF
)

# SUBMIT  - SIGNATURE LEVELS


urlpatterns = [
    path('sign_a/<int:pk>/',RejectSign_AApiview_APF.as_view()),
    path('sign_b/<int:pk>/',RejectSign_BApiview_APF.as_view()),
    path('sign_c/<int:pk>/',RejectSign_CApiview_APF.as_view())
]

