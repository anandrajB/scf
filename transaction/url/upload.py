from django.urls import path
from django.urls.conf import include
from accounts.views import index
from transaction.api.ProgramTransition import (
   UploadSign_AApiview,
   UploadSign_BApiview,
   UploadSign_CApiview
)

# -----------------------------------------------------------------------------

# UPLOAD - SIGNATURES URLS

# -----------------------------------------------------------------------------


urlpatterns = [
    path('sign_a/<int:pk>/',UploadSign_AApiview.as_view()),
    path('sign_b/<int:pk>/',UploadSign_BApiview.as_view()),
    path('sign_c/<int:pk>/',UploadSign_CApiview.as_view())
]



