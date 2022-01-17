from django import urls
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from accounts.views import SignatureUpdateApiview , SignatureUpdateSign_bApiview , SignatureUpdateSign_cApiview
from accounts.views import index

# SUBMIT  - SIGNATURE LEVELS


urlpatterns = [
    path('sign_a/<int:pk>/',SignatureUpdateApiview.as_view()),
    path('sign_b/<int:pk>/',SignatureUpdateSign_bApiview.as_view()),
    path('sign_c/<int:pk>/',SignatureUpdateSign_cApiview.as_view())
]



