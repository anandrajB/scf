from django import urls
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
# from accounts.views import SignatureUpdateApiview , SignatureUpdateSign_bApiview , SignatureUpdateSign_cApiview
from accounts.views import index
from transaction.views import (
    RejectSign_AApiview,
    RejectSign_BApiview,
    RejectSign_CApiview
)

# SUBMIT  - SIGNATURE LEVELS


urlpatterns = [
    path('sign_a/<int:pk>/',RejectSign_AApiview.as_view()),
    path('sign_b/<int:pk>/',RejectSign_BApiview.as_view()),
    path('sign_c/<int:pk>/',RejectSign_CApiview.as_view())
]



