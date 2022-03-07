from django.urls import path
from django.urls.conf import include
from accounts.views import index
from transaction.api.InvoiceTransition import (
    SubmitTransitionSign_AApiview_APF,
    SubmitTransitionSign_BApiview_APF,
    SubmitTransitionSign_CApiview_APF
)

# SUBMIT  - SIGNATURE LEVELS


urlpatterns = [
    path('sign_a/<int:pk>/',SubmitTransitionSign_AApiview_APF.as_view()),
    path('sign_b/<int:pk>/',SubmitTransitionSign_BApiview_APF.as_view()),
    path('sign_c/<int:pk>/',SubmitTransitionSign_CApiview_APF.as_view())
]

