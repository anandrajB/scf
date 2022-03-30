from django.urls import path
from django.urls.conf import include
from transaction.api.ProgramTransition import (
   ApproveSign_AApiView,
   ApproveSign_BApiView,
   ApproveSign_CApiView
)

# APPROVE - SIGNATURE LEVELS API URL'S


urlpatterns = [
    path('sign_a/<int:pk>/',ApproveSign_AApiView.as_view()),
    path('sign_b/<int:pk>/',ApproveSign_BApiView.as_view()),
    path('sign_c/<int:pk>/',ApproveSign_CApiView.as_view())
]



