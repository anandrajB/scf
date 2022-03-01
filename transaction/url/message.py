from django.urls import path
from django.urls.conf import include
from transaction.views import (
    InboxListApiview ,
    SentListApiview,
    DraftListApiview
)

# -----------------------------------------------------------------------------

# URLS FOR MESSAGE - INBOX , DRAFT , SENT

# -----------------------------------------------------------------------------


urlpatterns = [
    path('inbox/',InboxListApiview.as_view()),
    path('sent/',SentListApiview.as_view()),
    path('draft/',DraftListApiview.as_view()),
]
