from django.urls import path
from django.urls.conf import include
from accounts.views import index
from transaction.api.InvoiceTransition import (
    ArchiveTransition_APF_SignA,
    ArchiveTransition_APF_SignB,
    ArchiveTransition_APF_SignC,

)

# ARCHEIVE URLS


urlpatterns = [
    path('sign_a/<int:pk>/',ArchiveTransition_APF_SignA.as_view()),
    path('sign_b/<int:pk>/',ArchiveTransition_APF_SignB.as_view()),
    path('sign_c/<int:pk>/',ArchiveTransition_APF_SignC.as_view())
]

