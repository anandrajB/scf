from django import urls
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
# from accounts.views import SignatureUpdateApiview , SignatureUpdateSign_bApiview , SignatureUpdateSign_cApiview
from accounts.views import index
from transaction.views import (
    SubmitTransitionSign_AApiview,
    SubmitTransitionSign_BApiview,
    SubmitTransitionSign_CApiview
)

# SUBMIT  - SIGNATURE LEVELS


urlpatterns = [
    path('sign_a/<int:pk>/',SubmitTransitionSign_AApiview.as_view()),
    path('sign_b/<int:pk>/',SubmitTransitionSign_BApiview.as_view()),
    path('sign_c/<int:pk>/',SubmitTransitionSign_CApiview.as_view())
]



