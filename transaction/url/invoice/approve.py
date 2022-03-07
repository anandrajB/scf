from django.urls import path
from django.urls.conf import include
from accounts.views import index
from transaction.api.InvoiceTransition import (
    ApproveTransiton_SignA_APF,
    ApproveTransiton_SignB_APF,
    ApproveTransiton_SignC_APF
)

# SUBMIT  - SIGNATURE LEVELS


urlpatterns = [
    path('sign_a/<int:pk>/',ApproveTransiton_SignA_APF.as_view()),
    path('sign_b/<int:pk>/',ApproveTransiton_SignB_APF.as_view()),
    path('sign_c/<int:pk>/',ApproveTransiton_SignC_APF.as_view())
]

