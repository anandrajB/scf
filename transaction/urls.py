from django.urls import path , include
from .views import (
    ProgramListApiView, 
    ProgramCreateApiView ,
    ProgramUpdateDeleteApiview,
    deleted,
    submit_rejected,
    submitted,
    submitted_level_1,
    submitted_level_2,
    submitted_level_3,
    SignatureList,
)
from graphene_django.views import GraphQLView
# from .schema import schema

urlpatterns = [
    path('program/',ProgramCreateApiView.as_view(),name='pros'),
    path('program/<int:pk>/',ProgramUpdateDeleteApiview.as_view(),name='program-update'),
    path('program-list/',ProgramListApiView.as_view(),name='pro-list'),
    path('program/transition/delete/<int:pk>/', deleted,),
    path('program/transition/submit/<int:pk>/',submitted),
    # path('program/transition/sign_a/<int:pk>/', submitted_level_1),
    # path('program/transition/sign_b/<int:pk>/', submitted_level_2),
    # path('program/transition/sign_c/<int:pk>/', submitted_level_3),
    # path('program/transition/submit/reject/<int:pk>/', submit_rejected),
    path('sign/',SignatureList.as_view(),name='signatures'),
    path('program/approve/',include('transaction.urls1'),name='program-transition-approvals'),
    path('messages/',include('transaction.urls2')),
    
]