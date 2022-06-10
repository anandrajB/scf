from django.urls import path, include
from transaction.api.InvoiceTransition import (
    InvoiceOverdueTransitionApi,
    InvoiceSettleTransitionApi,
    InvoiceSubmitTransitionApiview,
    InvoiceRejectTransitionApiView,
    InvoiceApproveTransitionApiView,
    InvoiceArchiveTransitionApi,
    InvoiceRequestFinanceTransitionApi,
    InvoiceReturnTransitionApiView
)
from .views import (
    CounterPartyApiview,
    InvoiceCreateApiView,
    InvoiceUpdateDeleteApiview,
    InvoiceUploadCreateApiView,
    InvoiceUploadUpdateDeleteApiview,
    ProgramCreateApiView,
    ProgramUpdateDeleteApiview,
    PairingApiview,
    PairingUpdateapiview,
    CounterPartyUpdateapiview,
    FileUploadAPIView,
    EnquiryApiView,
    TestApiview,
    WorkFlowItemUpdateApi,
    WorkEventsUpdateApi,
    InboxNotificationCountApiView,
    MiscApiView
 
)
from transaction.api.InvoiceUploadTransition import (
    InvoiceUploadReturnTransitionview, 
    InvoiceUploadTransitionApiView
)
from graphene_django.views import GraphQLView
from .schema import schema
from transaction.api.ProgramTransition import (
    ProgramSubmitTransitionApiview , 
    ProgramApproveTransitionApiview , 
    ProgramAcceptTransitionApiview , 
    ProgramRejectTransitionApiview,
    ProgramTransitionDeleteApiview,
    ProgramReturnTransitionview
)
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [


    #-- PROGRAM CRUD URLS
    path('program/', ProgramCreateApiView.as_view(), name='program-create-api'),
    path('program/<int:pk>/', ProgramUpdateDeleteApiview.as_view(),name='program-update'),

    #--COUNTERPARTY CRUD URLS
    path('counterparty/', CounterPartyApiview.as_view(),name='counter-party-create'),
    path('counterparty/<int:pk>/', CounterPartyUpdateapiview.as_view(),name='counterparty-update'),

    #--INVOICE CRUD URLS
    path('invoice/', InvoiceCreateApiView.as_view(), name='invoice-manual-no-set(lifecycle)-create-api'),
    path('invoice/<int:pk>/', InvoiceUpdateDeleteApiview.as_view(),name='invoice-update'),
    
    #--INVOICE MANUAL UPLOAD CRUD URLS
    path('invoiceupload/',InvoiceUploadCreateApiView.as_view(),name='invoice-manual-upload-create'),
    path('invoiceupload/<int:pk>/', InvoiceUploadUpdateDeleteApiview.as_view(),name='invoiceupload-update'),

    # INVOICE CSV UPLOAD
    path('invoicecsvupload/', FileUploadAPIView.as_view(), name='invoice-csv-upload'),
    
    #--PAIRING'S CRUD URLS
    path('pairing/',PairingApiview.as_view(),name='pairing-create-list'),
    path('pairing/<int:pk>/',PairingUpdateapiview.as_view(),name='pairing-update'),

    #--MESSAGE INBOX
    path('messages/', include('transaction.message'),name = 'message-inbox-urls'),
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema),name ='GRAPH_QL URL'),

    #-- OTHER
    path('test/',TestApiview.as_view(),name='test'),
    path('enquiry/',EnquiryApiView.as_view(),name='enquiry-api'),
    path('workflowitem/<int:pk>/',WorkFlowItemUpdateApi.as_view(),name='workflowitem-update-api'),
    path('workevents/<int:pk>/',WorkEventsUpdateApi.as_view() , name = 'workevent_update_api'),
    path('notification/',InboxNotificationCountApiView.as_view(),name='notification-api-unread-messages-count'),
    path('choices/',MiscApiView.as_view(),name = 'interest and rate_type list api '),

    #### TRANSITIONS ####

    # PROGRAM TRANSITIONS
    
    path('program/transition/delete/<int:pk>/',ProgramTransitionDeleteApiview.as_view(), name='program-delete-transition'),
    path('program/transition/return/<int:pk>/',ProgramReturnTransitionview.as_view() , name = 'program-return-RETURN'),
    path('program/transition/submit/<int:pk>/',ProgramSubmitTransitionApiview.as_view(), name='initial-submit-transition-SUBMIT'),
    path('program/transition/reject/<int:pk>/',ProgramRejectTransitionApiview.as_view(), name='initial-reject-transition-REJECT'),
    path('program/transition/accept/<int:pk>/',ProgramAcceptTransitionApiview.as_view(), name='initial-accept-transition-ACCEPT'),
    path('program/transition/approve/<int:pk>/',ProgramApproveTransitionApiview.as_view(), name='initial-approve-transition-APPROVE-bank_user'),
    
    
    #---INVOICE TRANSITIONS
    path('invoice/transition/approve/<int:pk>/',InvoiceApproveTransitionApiView.as_view(), name='invoice-approve-transition'),
    path('invoice/transition/submit/<int:pk>/',InvoiceSubmitTransitionApiview.as_view(), name='invoice-submit-transition'),
    path('invoice/transition/reject/<int:pk>/',InvoiceRejectTransitionApiView.as_view(), name='invoice-reject-transition'),
    path('invoice/transition/archive/<int:pk>/',InvoiceArchiveTransitionApi.as_view(), name='invoice-archive-transition'),
    path('invoice/transition/RQF/<int:pk>/',InvoiceRequestFinanceTransitionApi.as_view(), name='invoice-request-finance-transition'),
    path('invoice/transition/return/<int:pk>/', InvoiceReturnTransitionApiView.as_view(),name='invoice-return-transition'),
    path('invoice/transition/settle/<int:pk>/', InvoiceSettleTransitionApi.as_view(),name='invoice-settle-transition'),
    path('invoice/transition/overdue/<int:pk>/', InvoiceOverdueTransitionApi.as_view(),name='invoice-overdue-transition'),

    
    #--INVOICE_UPLOAD TRANSITION
    path('invoiceupload/transition/submit/<int:pk>/',InvoiceUploadTransitionApiView.as_view(), name='invoice-upload-submit'),
    path('invoiceupload/transition/return/<int:pk>/',InvoiceUploadReturnTransitionview.as_view(), name='invoice-upload-return'),
    
] 