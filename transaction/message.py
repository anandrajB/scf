from django.urls import path
from django.urls.conf import include
from transaction.views import (
    InboxListApiview ,
    SentListApiview,
    DraftListApiview,
    AwaitingApprovalMessageApiView,
    SentAwaitingSignApiview,
    WorkEventHistoryListAPI,
)

# ------------------------------------------------------------------------------------------

# URLS FOR MESSAGE API'S - INBOX , DRAFT , SENT , AWAITING_FOR_SIGN , WORKFLOW_HISTORY

# -------------------------------------------------------------------------------------------


urlpatterns = [
    path('inbox/',InboxListApiview.as_view()),
    path('sent/',SentListApiview.as_view()),
    path('draft/',DraftListApiview.as_view()),
    path('aw_ap/',AwaitingApprovalMessageApiView.as_view()),
    path('sent_awap/',SentAwaitingSignApiview.as_view()),
    path('workflow-history/',WorkEventHistoryListAPI.as_view(),name='workflow_history'),

]
