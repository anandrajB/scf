from rest_framework.pagination import PageNumberPagination
from accounts.models import Currencies, Parties
import datetime
from accounts.permission.base_permission import Is_Buyer, Is_Bank
from transaction.FSM.Invoice import InvoiceFlow
from transaction.FSM.invoice_bank import InvoiceBankFlow 
from .models import (
    InterestChoice,
    InterestRateType,
    Invoices,
    Invoiceuploads,
    Pairings,
    Programs,
    workevents,
    workflowitems,
)
from rest_framework import generics
import pandas as pd
from django.db.models import Q
from accounts.permission.program_permission import *
from accounts.permission.upload_permissions import *
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveUpdateAPIView
)
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .serializer import (
    CounterPartyListSerializer,
    CounterPartySerializer,
    Interestchoiceserializer,
    Interestratetypechoiceserializer,
    InvoiceCreateserializer,
    InvoiceSerializer,
    InvoiceUploadlistserializer,
    InvoiceUploadserializer,
    PairingSerializer,
    ProgramListserializer,
    Programcreateserializer,
    WorkEventHistorySerializer,
    Workeventsmessageserializer,
    Workeventsserializer,
    Workflowitemsupdateserializer,
    Workitemsmessagesawapserializer,
    WorkFlowitemsEnquirySerializer,
    Workitemserializer,
    csvserializer
)
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status



# BASE USER MODEL

User = get_user_model()



# -----------------------------------------------------------------------------------------------------------------------------

# POLYMORPHIC SETUP - PROGRAM'S

# -----------------------------------------------------------------------------------------------------------------------------


class ProgramCreateApiView(ListCreateAPIView):
    queryset = Programs.objects.all()
    serializer_class = Programcreateserializer
    permission_classes = [Is_Buyer | Is_Bank]

    def get_queryset(self):
        user = self.request.user
        if user.party.party_type == "BANK":
            queryset = Programs.objects.all().order_by('created_date')
        else:
            queryset = Programs.objects.filter(party=user.party).order_by('created_date')
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProgramListserializer(queryset, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        serializer = Programcreateserializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(from_party=user.party, user=user,
                            to_party=user.party, event_user=user, party=user.party)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "failure", "data": serializer.errors}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class ProgramUpdateDeleteApiview(RetrieveUpdateDestroyAPIView):
    queryset = Programs.objects.all()
    serializer_class = ProgramListserializer
    permission_classes = [Is_Buyer | Is_Bank]

    def retrieve(self, request, pk=None):
        queryset = Programs.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ProgramListserializer(user)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        queryset = Programs.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ProgramListserializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "failure", "data": serializer.errors}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


# -----------------------------------------------------------------------------------------------------------------------------

# POLYMORPHIC SETUP - INVOICE'S (manual create)

# -----------------------------------------------------------------------------------------------------------------------------


class InvoiceCreateApiView(ListCreateAPIView):
    queryset = Invoices.objects.all()
    serializer_class = InvoiceCreateserializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, request):
        user = request.user
        if user.party.party_type == "BANK" or user.party.party_type == "BUYER":
            queryset = Invoices.objects.all()
        else:
            queryset = Invoices.objects.filter(party=user.party)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset(request)
        serializer = InvoiceSerializer(queryset, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        serializer = InvoiceCreateserializer(data=request.data)
        if serializer.is_valid():
            serializer.save(event_user=user,
                            from_party=user.party, to_party=user.party)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "failure", "data": serializer.errors},status=status.HTTP_204_NO_CONTENT)


class InvoiceUpdateDeleteApiview(RetrieveUpdateDestroyAPIView):
    queryset = Invoices.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        queryset = Invoices.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = InvoiceSerializer(user)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        queryset = Invoices.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = InvoiceSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "failure", "data": serializer.errors}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


# -----------------------------------------------------------------------------------------------------------------------------

# POLYMORPHIC SETUP - INVOICE UPLOAD

# -----------------------------------------------------------------------------------------------------------------------------


class InvoiceUploadCreateApiView(ListCreateAPIView):
    queryset = Invoiceuploads.objects.all()
    serializer_class = InvoiceUploadserializer
    permission_classes = [IsAuthenticated]
    
    # list based on completed status
    def get_queryset(self, request):
        qs = Invoiceuploads.objects.filter(workflowitems__user__party=request.user.party)
        type = request.GET.get("type", "")
        if type == "yes":
            qs = Invoiceuploads.objects.filter(workflowitems__user__party=request.user.party,is_finished = True)
        elif type == "no":
            qs = Invoiceuploads.objects.filter(workflowitems__user__party=request.user.party,is_finished = False)
        return qs


    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset(request)
        serializer = InvoiceUploadlistserializer(queryset, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        serializer = InvoiceUploadserializer(data=request.data)
        if serializer.is_valid():
            serializer.save(event_user=user, to_party=user.party,
                            from_party=user.party)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "failure", "data": serializer.errors},status = status.HTTP_204_NO_CONTENT)


class InvoiceUploadUpdateDeleteApiview(RetrieveUpdateDestroyAPIView):
    queryset = Invoiceuploads.objects.all()
    serializer_class = InvoiceUploadlistserializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        queryset = Invoiceuploads.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = InvoiceUploadlistserializer(user)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        queryset = Invoiceuploads.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = InvoiceUploadlistserializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "failure", "data": serializer.errors}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


# -----------------------------------------------------------------------------------------------------------------------------------------

# MESSAGING API - WORK_EVENTS

# -----------------------------------------------------------------------------------------------------------------------------------------


class InboxListApiview(APIView, PageNumberPagination):
    permission_classes = [IsAuthenticated]

    def get_queryset(self, request):
        queryset = workflowitems.objects.all()
        user = request.user
        record_type = request.GET.get("record_type", "")

        if record_type == "PROGRAM":
            queryset = workflowitems.objects.filter(
                current_to_party__name__contains=self.request.user.party.name, type="PROGRAM").exclude(interim_state='DRAFT').order_by('created_date')

        elif record_type == "INVOICE":
            queryset = workflowitems.objects.filter(Q(interim_state='AWAITING_BUYER_APPROVAL') | Q(interim_state='APPROVED_BY_BUYER') | Q(
                interim_state='REJECTED_BY_BUYER'), current_to_party__name__contains=user.party.name, type="INVOICE").order_by('created_date')

        elif record_type == "FINANCE_REQUEST":
            queryset = workflowitems.objects.filter(Q(interim_state='FINANCE_REQUESTED') | Q(interim_state='FINANCE_REJECTED') | Q(
                interim_state='FINANCED'), current_to_party__name__contains=user.party.name, type="INVOICE").order_by('created_date')
        
        elif record_type == "AW_SIGN":
            queryset = workflowitems.objects.filter(current_from_party__name__contains=request.user.party.name, next_available_transitions__isnull='')

        return queryset.filter(current_to_party__name__contains=user.party.name).exclude(Q(interim_state='DRAFT') | Q(interim_state='COMPLETED')).order_by('created_date')

    def get(self, request, *args, **kwargs):
        datas = self.get_queryset(request)
        results = self.paginate_queryset(datas, request)
        serializer = Workitemsmessagesawapserializer(results, many=True)
        return self.get_paginated_response(serializer.data)



# SENT API

class SentListApiview(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self, request):
        queryset = workevents.objects.all()
        user = self.request.user
        record_type = request.GET.get("record_type", "")
        if record_type == "PROGRAM":
            queryset = workevents.objects.filter(from_party__name__contains=user.party.name, type='PROGRAM',
                                                 final="YES").exclude(interim_state='DRAFT').order_by('created_date')

        elif record_type == "INVOICE":
            queryset = workevents.objects.filter(Q(interim_state='AWAITING_BUYER_APPROVAL') | Q(interim_state='APPROVED_BY_BUYER') | Q(
                interim_state='REJECTED_BY_BUYER'), from_party__name__contains=user.party.name, type='INVOICE',  final="YES").order_by('created_date')

        elif record_type == "FINANCE_REQUEST":
            queryset = workevents.objects.filter(Q(interim_state='FINANCE_REQUESTED') | Q(interim_state='FINANCE_REJECTED') | Q(
                interim_state='FINANCED'), from_party__name__contains=user.party.name, type='INVOICE',  final="YES").order_by('created_date')
        
        

        return queryset.filter(from_party__name__contains=user.party.name, final="YES").exclude(interim_state='DRAFT').order_by('created_date')

    def list(self, request, *args, **kwargs):
        var = self.get_queryset(request)
        serializer = Workeventsmessageserializer(var, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


# SENT AWAITING SIGN API

class SentAwaitingSignApiview(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self, request):
        queryset = workflowitems.objects.all()
        user = self.request.user
        record_type = request.GET.get("record_type", "")
        if record_type == "PROGRAM":
            queryset = workflowitems.objects.filter(current_from_party__name__contains=user.party.name, type='PROGRAM',
                                                    next_available_transitions__isnull='').exclude(interim_state='DRAFT').order_by('created_date')

        elif record_type == "INVOICE":
            queryset = workflowitems.objects.filter(Q(interim_state='AWAITING_BUYER_APPROVAL') | Q(interim_state='APPROVED_BY_BUYER') | Q(
                interim_state='REJECTED_BY_BUYER'), current_from_party__name__contains=user.party.name, type='INVOICE', next_available_transitions__isnull='').order_by('created_date')

        elif record_type == "FINANCE_REQUEST":
            queryset = workflowitems.objects.filter(Q(interim_state='FINANCE_REQUESTED') | Q(interim_state='FINANCE_REJECTED') | Q(
                interim_state='FINANCED'), current_from_party__name__contains=user.party.name, type='INVOICE', next_available_transitions__isnull='').order_by('created_date')

        return queryset.filter(current_from_party__name__contains=user.party.name, next_available_transitions__isnull='').exclude(interim_state='DRAFT').order_by('created_date')

    def list(self, request, *args, **kwargs):
        var = self.get_queryset(request)
        serializer = Workitemsmessagesawapserializer(var, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


# DRAFT API VIEW

class DraftListApiview(ListAPIView):
    permission_classes = [IsAuthenticated]


    def list(self, request, *args, **kwargs):
        var = workflowitems.objects.filter(current_from_party__name__contains=self.request.user.party.name,
                                           initial_state='DRAFT', interim_state='DRAFT').order_by('created_date')
        serializer = Workitemsmessagesawapserializer(var, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


# AWAITING APPROVAL API

class AwaitingApprovalMessageApiView(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemsmessagesawapserializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        var = workflowitems.objects.filter(
            current_from_party__name__contains=request.user.party.name, next_available_transitions__isnull='')
        serializer = Workitemsmessagesawapserializer(var, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


# TEST PURPOSE

class TestApiview(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"data":"FINFLO TESTING"})



# -----------------------------------------------------------------------------------------------------------------------------

# PAIRING CREATE API VIEW

# -----------------------------------------------------------------------------------------------------------------------------


class PairingApiview(APIView):
    queryset = Pairings.objects.all()
    serializer_class = PairingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PairingSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"Status": "Failed", "data": serializer.errors}, status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self, request):
        user = self.request.user
        data = self.request.query_params.get('pg_id')
        if data is not None:
            qs = Pairings.objects.filter(program_id=data)
        else:
            qs = Pairings.objects.filter(counterparty_id=user.party.id)
        return qs

    def get(self, request):
        model1 = self.get_queryset(self)
        serializer = PairingSerializer(model1, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


# PAIRING UPDATE API VIEW

class PairingUpdateapiview(RetrieveUpdateDestroyAPIView):
    queryset = Pairings.objects.all()
    serializer_class = PairingSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        queryset = Pairings.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = PairingSerializer(user)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        queryset = Pairings.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = PairingSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "failure", "data": serializer.errors}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


# -----------------------------------------------------------------------------------------------------------------------------

# COUNTERPARTY API VIEW

# -----------------------------------------------------------------------------------------------------------------------------


class CounterPartyApiview(APIView):
    queryset = Parties.objects.all()
    serializer_class = CounterPartySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Parties.objects.filter(party_type="SELLER")
        ser = CounterPartyListSerializer(queryset, many=True)
        return Response({"Status": "Success", "data": ser.data}, status=status.HTTP_201_CREATED)

    def post(self, request):
        serializer = CounterPartySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"Status": "Success", }, status=status.HTTP_201_CREATED)
        return Response({"Status": "Failed", "data": serializer.errors}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


# COUNTERPARTY UPDATE API VIEW

class CounterPartyUpdateapiview(RetrieveUpdateDestroyAPIView):
    queryset = Pairings.objects.all()
    serializer_class = PairingSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        queryset = Pairings.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = PairingSerializer(user)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        queryset = Pairings.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = PairingSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "failure", "data": serializer.errors}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)



# -----------------------------------------------------------------------------------------------------------------------------

# WORK EVENT HISTORY API

# -----------------------------------------------------------------------------------------------------------------------------

class WorkEventHistoryListAPI(APIView):
    queryset = workevents.objects.all()
    serializer_class = WorkEventHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, request):
        user = self.request.user
        data = self.request.query_params.get('wf_item')
        if data is not None:
            qs = workevents.objects.filter(workitems=data)
        else:
            qs = workevents.objects.all()
        return qs

    def get(self, request):
        queryset = self.get_queryset(self)
        ser = WorkEventHistorySerializer(queryset, many=True)
        return Response({"Status": "Success", "data": ser.data}, status=status.HTTP_201_CREATED)




# -----------------------------------------------------------------------------------------------------------------------------

# ENQUIRY API VIEW

# -----------------------------------------------------------------------------------------------------------------------------


class EnquiryApiView(ListAPIView):
    queryset =  workflowitems.objects.all()
    serializer_class = WorkFlowitemsEnquirySerializer

    def get(self, request):
        model = qs = workflowitems.objects.filter(current_from_party = request.user.party)
        serializer = WorkFlowitemsEnquirySerializer(model, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


# -----------------------------------------------------------------------------------------------------------------------------

# MISC

# -----------------------------------------------------------------------------------------------------------------------------



## INVOICE UPLOAD CSV API VIEW


class FileUploadAPIView(APIView):
    queryset = None
    serializer_class = csvserializer

    def post(self, request, *args, **kwargs):
        serializer = csvserializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['invoice']

        user , party = request.user , request.user.party
        reader = pd.read_csv(file)
        
        format = "%d-%m-%Y"
        arr = []
        brr = []
        for index , row in reader.iterrows():
            
            buyer_name , buyer_id = row['buyer_name'] , row['buyer_id'] 
        
            # base checks from csv
            pair =  Pairings.objects.filter(id = buyer_id ,counterparty_id=party.id, program_id__party__name=buyer_name)
            currency = Currencies.objects.filter(description = row['financing_currency'])
            currency_2 = Currencies.objects.filter(description = row['settlement_currency'])
            qs = datetime.datetime.strptime(row['invoice_date'],format)
            
            if (pair and currency and currency_2).exists() :
                arr.append(pair)
            
                data = {
                                    'buyerId': buyer_id,
                                    'buyerName': buyer_name,
                                    'invoiceNo': row['invoice_no'],
                                    'invoiceDate': row['invoice_date'],
                                    'invoiceAmount': row['invoice_amount'],
                                    'dueDate': row['due_date'],
                                    'financingCurrency': row['financing_currency'],
                                    'settlementCurrency': row['settlement_currency'],
                                    'invoiceType' : row['financing_currency'],
                                    'counterparty_id': party.name
                }
                
                brr.append(data)
            else:
                data = {
                                    'buyerId': buyer_id,
                                    'buyerName': buyer_name,
                                    'invoiceNo': row['invoice_no'],
                                    'invoiceDate': row['invoice_date'],
                                    'invoiceAmount': row['invoice_amount'],
                                    'dueDate': row['due_date'],
                                    'financingCurrency': row['financing_currency'],
                                    'settlementCurrency': row['settlement_currency'],
                                    'invoiceType' : row['financing_currency'],
                                    'counterparty_id': party.name
                }
                brr.append(data)
        # print("len of csv",len(reader))
        # print("len of pair",len(arr))
        if len(reader) == len(arr):
            
            uploads = Invoiceuploads.objects.create(invoices = brr , program_type = "APF" , is_finished = True)
            # print("it works")
            uploads.save()
            work = workflowitems.objects.create(
                uploads=uploads, current_from_party=user.party,current_to_party=user.party, user=user , type="UPLOAD")
            event = workevents.objects.create( event_user = user , type = "UPLOAD",
                workitems=work, from_party=user.party, to_party=user.party) 
            work.save()
            event.save()
        else:
            uploads = Invoiceuploads.objects.create(invoices = brr , program_type = "APF" , is_finished = False) 
            uploads.save( )
            work = workflowitems.objects.create(
                uploads=uploads, current_from_party=user.party,current_to_party=user.party, user=user , type="UPLOAD")
            event = workevents.objects.create( event_user = user , type = "UPLOAD",
                workitems=work, from_party=user.party, to_party=user.party) 
            work.save()
            event.save()
            
        return Response({"status": "Invoice uploaded successfully"},status= status.HTTP_200_OK)
            


## WORKFLOWITEM UPDATE API 

class WorkFlowItemUpdateApi(RetrieveUpdateAPIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer


    def update(self, request, pk=None):
        queryset = workflowitems.objects.all()
        state = request.data.get('state')
        user = get_object_or_404(queryset, pk=pk)
        serializer = Workitemserializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            obj = generics.get_object_or_404(queryset, id=serializer.data['id'])
            flow = InvoiceBankFlow(obj)
            if state == "FINANCED":
                flow.approve_invoice(request)
                obj.save()
                return Response({"status": "success", "data": "INVOICE FINANCED"}, status=status.HTTP_200_OK)
            elif state == "REJECTED":
                flow.reject_invoice(request)
                obj.save()
                return Response({"status": "success", "data": "INVOICE REJECTED"}, status=status.HTTP_200_OK)
            elif state == "SETTLED":
                flow.settle_invoice(request)
                obj.save()
                return Response({"status": "success", "data": "INVOICE SETTLED"}, status=status.HTTP_200_OK)
            elif state == "OVERDUE":
                flow.overdue_invoice(request)
                obj.save()
                return Response({"status": "success", "data": "INVOICE OVERDUED"}, status=status.HTTP_200_OK)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "failure", "data": serializer.errors}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)




### INBOX NOTIFICATION COUNT API

class InboxNotificationCountApiView(APIView):
    queryset =  workflowitems.objects.all()

    def get(self, request):
        model1 = workflowitems.objects.filter(current_from_party = request.user.party,is_read = True).count()
        model2 = workflowitems.objects.filter(current_from_party = request.user.party,is_read = True , interim_state = "DRAFT" ).count()
        model3 = workevents.objects.filter(from_party = request.user.party,is_read = True).count()
        return Response({"status": "success", "inbox_count": model1 , "draft_count" : model2,"sent_count": model3}, status=status.HTTP_200_OK)




## WORKEVENTS UPDATE API VIEW

class WorkEventsUpdateApi(RetrieveUpdateDestroyAPIView):
    queryset = workevents.objects.all()
    serializer_class = Workeventsserializer
    permission_classes = [IsAuthenticated]

    def update(self, request, pk=None):
        queryset = workevents.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = Workeventsserializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "failure", "data": serializer.errors}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)



class MiscApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = self.request.query_params.get('type')
        if data == "IC":
            qs = InterestChoice.objects.all()
            ser = Interestchoiceserializer(qs, many=True)
        else:
            qs = InterestRateType.objects.all()
            ser = Interestratetypechoiceserializer(qs, many=True)
        return Response({"Status": "Success", "data": ser.data}, status=status.HTTP_200_OK)