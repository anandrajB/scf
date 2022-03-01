from django.urls import path
from django.urls.conf import include
from accounts.views import index
from transaction.api.ProgramTransition import (
    RejectSign_AApiview,
    RejectSign_BApiview,
    RejectSign_CApiview
)

# REJECT - SIGNATURE LEVELS


urlpatterns = [
    path('sign_a/<int:pk>/',RejectSign_AApiview.as_view()),
    path('sign_b/<int:pk>/',RejectSign_BApiview.as_view()),
    path('sign_c/<int:pk>/',RejectSign_CApiview.as_view())
]



