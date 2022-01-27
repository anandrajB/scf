from django.urls import path, include
from accounts.views import index
from .views import (
    ProgramListApiView,
    ProgramCreateApiView,
    ProgramUpdateDeleteApiview,
    SubmitTransitionApiView,
    ActionCreateApiView,
    ModelCreateApiview,
    RejectedSignApi,
    TransitionDeleteApiview
)
from graphene_django.views import GraphQLView
from .schema import schema

urlpatterns = [
    path('program/', ProgramCreateApiView.as_view(), name='pros'),
    path('program/<int:pk>/', ProgramUpdateDeleteApiview.as_view(),
         name='program-update'),
    path('program-list/', ProgramListApiView.as_view(), name='pro-list'),
    path('program/transition/delete/<int:pk>/',
         TransitionDeleteApiview.as_view(), name='delete-transition'),
    path('program/transition/submit/<int:pk>/',
         SubmitTransitionApiView.as_view(), name='initial-submit'),
    path('program/transition/reject/<int:pk>/',
         RejectedSignApi.as_view(), name='reject-transition'),
    path('program/transition/submit/', include('transaction.url.submit'),
         name='program-transition-approvals-SUBMIT'),
    path('program/transition/reject/', include('transaction.url.reject'),
         name='program-transition-reject-REJECT'),
    path('action/', ActionCreateApiView.as_view()),
    path('model/', ModelCreateApiview.as_view()),
    path('messages/', include('transaction.url.message')),
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema))
]
