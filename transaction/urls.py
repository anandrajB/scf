from django.urls import path, include
from accounts.views import index
from .views import (
    AcceptTransitionApiview,
    InvoiceListApiView,
    InvoiceUpdateDeleteApiview,
    ProgramListApiView,
    ProgramCreateApiView,
    ProgramUpdateDeleteApiview,
    SubmitTransitionApiView,
    ActionCreateApiView,
    ModelCreateApiview,
    RejectTransitionApiView,
    TransitionDeleteApiview,
    TestApiview,
    PairingApiview,
    PairingUpdateapiview,
    InvoiceCreateApiView
)
from graphene_django.views import GraphQLView
from .schema import schema

urlpatterns = [
    path('program/', ProgramCreateApiView.as_view(), name='program-create-api'),
    path('program/<int:pk>/', ProgramUpdateDeleteApiview.as_view(),name='program-update'),
    path('program-list/', ProgramListApiView.as_view(), name='program-list'),
    path('invoice/', InvoiceCreateApiView.as_view(), name='invoice-create-api'),
    path('invoice/<int:pk>/', InvoiceUpdateDeleteApiview.as_view(),name='invoice-update'),
    path('invoice-list/', InvoiceListApiView.as_view(), name='invoice-list'),
    path('pairing/',PairingApiview.as_view(),name='pairing-create-list'),
    path('pairing/<int:pk>/',PairingUpdateapiview.as_view(),name='pairing-update'),
    #--
    path('program/transition/delete/<int:pk>/',TransitionDeleteApiview.as_view(), name='delete-transition'),
    path('program/transition/submit/<int:pk>/',SubmitTransitionApiView.as_view(), name='initial-submit-transition'),
    path('program/transition/reject/<int:pk>/',RejectTransitionApiView.as_view(), name='initial-reject-transition'),
    path('program/transition/accept/<int:pk>/',AcceptTransitionApiview.as_view(), name='initial-accept-transition'),
    path('program/transition/submit/', include('transaction.url.submit'),name='program-transition-approvals-SUBMIT'),
    path('program/transition/reject/', include('transaction.url.reject'),name='program-transition-reject-REJECT'),
    path('program/transition/accept/', include('transaction.url.accept'),name='program-transition-accept-ACCEPT'),
    #---
    path('invoice/transition/delete/<int:pk>/',TransitionDeleteApiview.as_view(), name='delete-transition'),
    path('invoice/transition/submit/<int:pk>/',SubmitTransitionApiView.as_view(), name='initial-submit-transition'),
    path('invoice/transition/reject/<int:pk>/',RejectTransitionApiView.as_view(), name='initial-reject-transition'),
    path('invoice/transition/accept/<int:pk>/',AcceptTransitionApiview.as_view(), name='initial-accept-transition'),
    path('invoice/transition/submit/', include('transaction.url.submit'),name='invoice-transition-approvals-SUBMIT'),
    path('invoice/transition/reject/', include('transaction.url.reject'),name='invoice-transition-reject-REJECT'),
    path('invoice/transition/accept/', include('transaction.url.accept'),name='invoice-transition-accept-ACCEPT'),
    #--
    path('messages/', include('transaction.url.message'),name = 'message-inbox-urls'),
    path('action/', ActionCreateApiView.as_view()),
    path('model/', ModelCreateApiview.as_view()),
    path('test/',TestApiview.as_view()),
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema),name ='GRAPH_QL URL')
]
