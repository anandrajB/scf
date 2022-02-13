from django.urls import path
from django.urls.conf import include
from transaction.api.customertransition import (
   AcceptSign_AApiView,
   AcceptSign_BApiView,
   AcceptSign_CApiView
)

# ACCEPT - SIGNATURE LEVELS API URL'S


urlpatterns = [
    path('sign_a/<int:pk>/',AcceptSign_AApiView.as_view()),
    path('sign_b/<int:pk>/',AcceptSign_BApiView.as_view()),
    path('sign_c/<int:pk>/',AcceptSign_CApiView.as_view())
]



