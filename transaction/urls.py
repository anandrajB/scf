from django.urls import path, include
from .views import (
    ProgramListApiView,
    ProgramCreateApiView,
    ProgramUpdateDeleteApiview,
    deleted,
    rejected,
    rejected_level_1,
    rejected_level_2,
    rejected_level_3,
    accepted,
    accepted_level_1,
    accepted_level_2,
    accepted_level_3,
    submitted,
    submitted_level_1,
    submitted_level_2,
    submitted_level_3,
    SignatureList,
)
from graphene_django.views import GraphQLView
# from .schema import schema

urlpatterns = [
    path('program/', ProgramCreateApiView.as_view(), name='pros'),
    path('program/<int:pk>/', ProgramUpdateDeleteApiview.as_view(),
         name='program-update'),
    path('program-list/', ProgramListApiView.as_view(), name='pro-list'),
    path('program/transition/delete/<int:pk>/', deleted,),
    path('program/transition/submit/<int:pk>/', submitted),
    # SUBMIT URLS
    path('program/transition/submit/<int:pk>/', submitted),
    path('program/transition/submit_sign_a/<int:pk>/', submitted_level_1),
    path('program/transition/submit_sign_b/<int:pk>/', submitted_level_2),
    path('program/transition/submit_sign_c/<int:pk>/', submitted_level_3),
    # REJECT URLS
    path('program/transition/reject/<int:pk>/', rejected),
    path('program/transition/reject_sign_a/<int:pk>/', rejected_level_1),
    path('program/transition/reject_sign_b/<int:pk>/', rejected_level_2),
    path('program/transition/reject_sign_c/<int:pk>/', rejected_level_3),
    # ACCEPT URLS
    path('program/transition/accept/<int:pk>/', accepted),
    path('program/transition/accept_sign_a/<int:pk>/', accepted_level_1),
    path('program/transition/accept_sign_b/<int:pk>/', accepted_level_2),
    path('program/transition/accept_sign_c/<int:pk>/', accepted_level_3),
# <------------------------------------------------------------------------>
    path('sign/', SignatureList.as_view(), name='signatures'),
    path('program/approve/', include('transaction.urls1'),
         name='program-transition-approvals'),
    path('messages/', include('transaction.urls2')),

]
