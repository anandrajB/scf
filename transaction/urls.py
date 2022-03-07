from django.urls import path, include
from accounts.views import index
from rest_framework import routers

from transaction.api.InvoiceTransition import ( ApproveTransitionApiView, Archive_APIView_APF, REQ_FIN_TransitionAPIView ,
    RejectTransitionApiView_APF,
    SubmitTransitionApiView_APF
)
from .views import (
    InvoiceUpdateDeleteApiview,
    InvoiceUploadCreateApiView,
    InvoiceUploadListapiview,
    InvoiceUploadUpdateDeleteApiview,
    ProgramCreateApiView,
    ProgramUpdateDeleteApiview,
    TestApiview,
    PairingApiview,
    PairingUpdateapiview,
    InvoiceCreateApiView
)
from transaction.api.ProgramTransition import (
    AcceptTransitionApiview,
    ReturnTransitionview,
    TransitionDeleteApiview,
    RejectTransitionApiView,
    SubmitTransitionApiView,
    UploadSubmitTransitionApiView
)
from graphene_django.views import GraphQLView
from .schema import schema



router = routers.DefaultRouter()
router.register(r'invoiceupload',InvoiceUploadCreateApiView),

urlpatterns = [
    
    #-- PROGRAM URLS
    path('program/', ProgramCreateApiView.as_view(), name='program-create-api'),
    path('program/<int:pk>/', ProgramUpdateDeleteApiview.as_view(),name='program-update'),
    
    #--INVOICE URLS
    path('invoice/', InvoiceCreateApiView.as_view(), name='invoice-manual-create-api'),
    path('invoice/<int:pk>/', InvoiceUpdateDeleteApiview.as_view(),name='invoice-update'),
    
    #--INVOICE UPLOAD URLS
    path('', include(router.urls),name='invoice-upload-create-apiview'),
    path('invoiceupload/<int:pk>/', InvoiceUploadUpdateDeleteApiview.as_view(),name='invoiceupload-update'),
    
    #--PAIRING'S 
    path('pairing/',PairingApiview.as_view(),name='pairing-create-list'),
    path('pairing/<int:pk>/',PairingUpdateapiview.as_view(),name='pairing-update'),

    #--PROGRAM TRANSITIONS
    path('program/transition/delete/<int:pk>/',TransitionDeleteApiview.as_view(), name='delete-transition'),
    path('program/transition/submit/<int:pk>/',SubmitTransitionApiView.as_view(), name='initial-submit-transition-SUBMIT'),
    path('program/transition/reject/<int:pk>/',RejectTransitionApiView.as_view(), name='initial-reject-transition-REJECT'),
    path('program/transition/accept/<int:pk>/',AcceptTransitionApiview.as_view(), name='initial-accept-transition-ACCEPT'),
    path('program/transition/approve/<int:pk>/',ApproveTransitionApiView.as_view(), name='initial-approve-transition-APPROVE-bank_user'),
    path('program/transition/return/<int:pk>/',ReturnTransitionview.as_view() , name = 'program-return-RETURN'),
    path('program/transition/submit/', include('transaction.url.program.submit'),name='program-transition-submit-SUBMIT'),
    path('program/transition/reject/', include('transaction.url.program.reject'),name='program-transition-reject-REJECT'),
    path('program/transition/accept/', include('transaction.url.program.accept'),name='program-transition-accept-ACCEPT'),
    path('program/transition/approve/', include('transaction.url.program.approve'),name='program-transition-approve-APPROVE'),
    

    #---INVOICE TRANSITIONS
    path('invoice/transition/approve/<int:pk>/',ApproveTransitionApiView.as_view(), name='invoice-approve-transition'),
    path('invoice/transition/submit/<int:pk>/',SubmitTransitionApiView_APF.as_view(), name='initial-submit-transition'),
    path('invoice/transition/reject/<int:pk>/',RejectTransitionApiView_APF.as_view(), name='initial-reject-transition'),
    path('invoice/transition/archive/<int:pk>/',Archive_APIView_APF.as_view(), name='initial-archeive-transition'),
    path('invoice/transition/RF/<int:pk>/',REQ_FIN_TransitionAPIView.as_view(), name='initial-request-finance-transition'),
    path('invoice/transition/submit/', include('transaction.url.invoice.submit'),name='invoice-transition-SUBMIT'),
    path('invoice/transition/reject/', include('transaction.url.invoice.reject'),name='invoice-transition-reject-REJECT'),
    path('invoice/transition/approve/', include('transaction.url.invoice.approve'),name='invoice-transition-approve-APPROVE'),
    path('invoice/transition/RF/', include('transaction.url.invoice.requestfinance'),name='invoice-transition-requestfinance-RF'),
    path('invoice/transition/archive/', include('transaction.url.invoice.archieve'),name='invoice-transition-archieve-ARCHIEVE'),
    #--
    path('invoiceupload/transition/submit/<int:pk>/',UploadSubmitTransitionApiView.as_view(), name='invoice-upload-submit'),
    path('invoiceupload/transition/submit/', include('transaction.url.upload'),name='upload-transition-approvals-SUBMIT'),
    
    #--MESSAGE INBOX
    path('messages/', include('transaction.url.message'),name = 'message-inbox-urls'),
    path('test/<int:pk>/',TestApiview.as_view()),
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema),name ='GRAPH_QL URL')
]
