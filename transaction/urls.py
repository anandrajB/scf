from django.urls import path, include
from .views import (
    ProgramListApiView,
    ProgramCreateApiView,
    ProgramUpdateDeleteApiview,
    accepted,
    accepted_1,
    accepted_2,
    accepted_3,
    # deleted,
    # rejected,
    # rejected_level_1,
    # rejected_level_2,
    # rejected_level_3,
    # accepted,
    # accepted_level_1,
    # accepted_level_2,
    # accepted_level_3,
    # return_level_1,
    # return_level_2,
    # return_level_3,
    # submitted,
    # submitted_level_1,
    # submitted_level_2,
    # submitted_level_3,
    submitted,
    submitted_1,
    submitted_2,
    submitted_3,
    rejected, rejected_1, rejected_2,
    rejected_3,
    SignatureList,
)
from graphene_django.views import GraphQLView
# from .schema import schema

urlpatterns = [
    path('program/', ProgramCreateApiView.as_view(), name='pros'),
    path('program/<int:pk>/', ProgramUpdateDeleteApiview.as_view(),
         name='program-update'),
    path('program-list/', ProgramListApiView.as_view(), name='pro-list'),
    # path('program/transition/delete/<int:pk>/', deleted,),
    # path('program/transition/submit/<int:pk>/', submitted),
    # SUBMIT URLS
    # path('program/transition/submit/<int:pk>/', submitted),
    # path('program/transition/submit_sign_a/<int:pk>/', submitted_level_1),
    # path('program/transition/submit_sign_b/<int:pk>/', submitted_level_2),
    # path('program/transition/submit_sign_c/<int:pk>/', submitted_level_3),
    # # REJECT URLS
    # path('program/transition/reject/<int:pk>/', rejected),
    # path('program/transition/reject_sign_a/<int:pk>/', rejected_level_1),
    # path('program/transition/reject_sign_b/<int:pk>/', rejected_level_2),
    # path('program/transition/reject_sign_c/<int:pk>/', rejected_level_3),
    # # ACCEPT URLS
    # path('program/transition/accept/<int:pk>/', accepted),
    # path('program/transition/accept_sign_a/<int:pk>/', accepted_level_1),
    # path('program/transition/accept_sign_b/<int:pk>/', accepted_level_2),
    # path('program/transition/accept_sign_c/<int:pk>/', accepted_level_3),
    # # RETURN URLS
    # path('program/transition/return_1/<int:pk>', return_level_1),
    # path('program/transition/return_2/<int:pk>', return_level_2),
    # path('program/transition/return_3/<int:pk>', return_level_3),
    path('program/transition/submit/<int:pk>/', submitted),
    path('program/transition/submit_1/<int:pk>/', submitted_1),
    path('program/transition/submit_2/<int:pk>/', submitted_2),
    path('program/transition/submit_3/<int:pk>/', submitted_3),
    # <------------------------------------------------------------------------>
    path('program/transition/reject/<int:pk>/', rejected),
    path('program/transition/reject_1/<int:pk>/', rejected_1),
    path('program/transition/reject_2/<int:pk>/', rejected_2),
    path('program/transition/reject_3/<int:pk>/', rejected_3),
    # <------------------------------------------------------------------------>
    path('program/transition/accept/<int:pk>/', accepted),
    path('program/transition/accept_1/<int:pk>/', accepted_1),
    path('program/transition/accept_2/<int:pk>/', accepted_2),
    path('program/transition/accept_3/<int:pk>/', accepted_3),
    # <------------------------------------------------------------------------>
    path('sign/', SignatureList.as_view(), name='signatures'),
    path('program/approve/', include('transaction.urls1'),
         name='program-transition-approvals'),
    path('messages/', include('transaction.urls2')),

]
