from django.urls import path, include
from accounts.views import index
from rest_framework import routers
from .views import (
    InvoiceListApiView,
    InvoiceUpdateDeleteApiview,
    InvoiceUploadCreateApiView,
    InvoiceUploadListapiview,
    InvoiceUploadUpdateDeleteApiview,
    ProgramListApiView,
    ProgramCreateApiView,
    ProgramUpdateDeleteApiview,
    TestApiview,
    PairingApiview,
    PairingUpdateapiview,
    InvoiceCreateApiView
)
from transaction.api.customertransition import (
    AcceptTransitionApiview,
    TransitionDeleteApiview,
    RejectTransitionApiView,
    SubmitTransitionApiView,
    UploadSubmitTransitionApiView
)
from graphene_django.views import GraphQLView
from .schema import schema



router = routers.DefaultRouter()
router.register(r'upload',InvoiceUploadCreateApiView),

urlpatterns = [
    
    #-- PROGRAM URLS
    path('program/', ProgramCreateApiView.as_view(), name='program-create-api'),
    path('program/<int:pk>/', ProgramUpdateDeleteApiview.as_view(),name='program-update'),
    path('program-list/', ProgramListApiView.as_view(), name='program-list'),
    
    #--INVOICE URLS
    path('invoice/', InvoiceCreateApiView.as_view(), name='invoice-manual-create-api'),
    path('invoice/<int:pk>/', InvoiceUpdateDeleteApiview.as_view(),name='invoice-update'),
    path('invoice-list/', InvoiceListApiView.as_view(), name='invoice-list'),

    #--INVOICE UPLOAD URLS
    path('', include(router.urls),name='invoice-upload-create-apiview'),
    # path('invoiceupload/', InvoiceUploadCreateApiView.as_view(), name='invoice-upload-create-api'),
    path('invoiceupload/<int:pk>/', InvoiceUploadUpdateDeleteApiview.as_view(),name='invoiceupload-update'),
    path('invoiceupload/', InvoiceUploadListapiview.as_view(), name='invoice-upload-list'),
    path('pairing/',PairingApiview.as_view(),name='pairing-create-list'),
    path('pairing/<int:pk>/',PairingUpdateapiview.as_view(),name='pairing-update'),

    #--PROGRAM TRANSITIONS
    path('program/transition/delete/<int:pk>/',TransitionDeleteApiview.as_view(), name='delete-transition'),
    path('program/transition/submit/<int:pk>/',SubmitTransitionApiView.as_view(), name='initial-submit-transition'),
    path('program/transition/reject/<int:pk>/',RejectTransitionApiView.as_view(), name='initial-reject-transition'),
    path('program/transition/accept/<int:pk>/',AcceptTransitionApiview.as_view(), name='initial-accept-transition'),
    path('program/transition/submit/', include('transaction.url.submit'),name='program-transition-approvals-SUBMIT'),
    path('program/transition/reject/', include('transaction.url.reject'),name='program-transition-reject-REJECT'),
    path('program/transition/accept/', include('transaction.url.accept'),name='program-transition-accept-ACCEPT'),

    #---INVOICE TRANSITIONS
    path('invoice/transition/delete/<int:pk>/',TransitionDeleteApiview.as_view(), name='delete-transition'),
    path('invoice/transition/submit/<int:pk>/',SubmitTransitionApiView.as_view(), name='initial-submit-transition'),
    path('invoice/transition/reject/<int:pk>/',RejectTransitionApiView.as_view(), name='initial-reject-transition'),
    path('invoice/transition/accept/<int:pk>/',AcceptTransitionApiview.as_view(), name='initial-accept-transition'),
    path('invoice/transition/submit/', include('transaction.url.submit'),name='invoice-transition-approvals-SUBMIT'),
    path('invoice/transition/reject/', include('transaction.url.reject'),name='invoice-transition-reject-REJECT'),
    path('invoice/transition/accept/', include('transaction.url.accept'),name='invoice-transition-accept-ACCEPT'),
    #--
    path('upload/transition/submit/<int:pk>/',UploadSubmitTransitionApiView.as_view(), name='invoice-upload-submit'),
    path('upload/transition/submit/', include('transaction.url.upload'),name='upload-transition-approvals-SUBMIT'),
    
    #--MESSAGE INBOX
    path('messages/', include('transaction.url.message'),name = 'message-inbox-urls'),
    path('test/<int:pk>/',TestApiview.as_view()),
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema),name ='GRAPH_QL URL')
]
