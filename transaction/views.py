from accounts.models import Currencies, Parties
from accounts.permission.base_permission import Is_BankAdministrator, Is_Buyer
from .models import (
    Invoices,
    Invoiceuploads,
    Pairings,
    Programs,
    Transitionpartytype,
    workevents,
    workflowitems,
)
from django.db.models import Q
from accounts.permission.program_permission import *
from accounts.permission.upload_permissions import *
from django.shortcuts import render
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .serializer import (
    CounterPartyListSerializer,
    CounterPartySerializer,
    InvoiceCreateserializer,
    InvoiceSerializer,
    InvoiceUploadlistserializer,
    InvoiceUploadserializer,
    PairingSerializer,
    ProgramListserializer,
    Programcreateserializer,
    Workeventsmessageserializer,
    programupdateserilizer
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import generics


User = get_user_model()

# -----------------------------------------------------------------------------------------------------------------------------

# POLYMORPHIC SETUP - PROGRAM'S

# -----------------------------------------------------------------------------------------------------------------------------

class ProgramCreateApiView(ListCreateAPIView):
    queryset = Programs.objects.all()
    serializer_class = Programcreateserializer
    permission_classes = [IsAuthenticated , Is_Buyer]

    def get_queryset(self):
        user = self.request.user
        if user.is_administrator == True:
            queryset = Programs.objects.all()
        else:
            queryset = Programs.objects.filter(party=user.party)
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProgramListserializer(queryset,many=True,)
        return Response({"status": "success","data": serializer.data}, status=status.HTTP_200_OK)


    def post(self, request):
        user = request.user
        serializer = Programcreateserializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save(from_party = user.party, user = user , to_party = user.party,event_user = user , party = user.party)
            return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "failure", "data": serializer.errors},status=status.HTTP_406_NOT_ACCEPTABLE)



class ProgramUpdateDeleteApiview(APIView):
    serializer_class = programupdateserilizer
    permission_classes = [IsAuthenticated,Is_Buyer]

    def get(self, request, pk=None):
        queryset = Programs.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ProgramListserializer(user)
        return Response({"status": "success","data": serializer.data}, status=status.HTTP_200_OK)


    def put(self, request, pk, *args, **kwargs):
        queryset = Programs.objects.all()
        program = get_object_or_404(queryset, pk=pk)
        serializer = programupdateserilizer(program, request.data)
        if serializer.is_valid():
            serializer.save()
            mydata = serializer.data['comments']
            data = program.workflowitems.workflowevent.last()
            comment_Data = data.record_datas 
            comment_Data['comments'].append(mydata)
            # save the model 
            data.save()
            # qs.save()
            return Response({"status": "success","data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "Failed","data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        program = get_object_or_404(pk=pk)
        program.delete()
        return Response({"status": "success"},status=status.HTTP_200_OK)


# -----------------------------------------------------------------------------------------------------------------------------

# POLYMORPHIC SETUP - INVOICE'S (manual create)

# -----------------------------------------------------------------------------------------------------------------------------


class InvoiceCreateApiView(ListCreateAPIView):
    queryset = Invoices.objects.all()
    serializer_class = InvoiceCreateserializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.party.party_type == "BANK":
            queryset = Invoices.objects.all()
        else:
            queryset = Invoices.objects.filter(party = user.party)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = Invoices.objects.all()
        serializer = InvoiceSerializer(queryset, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = InvoiceCreateserializer(data=request.data)
        if serializer.is_valid():
            serializer.save(event_user = request.user)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "failure", "data": serializer.errors})



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
        return Response({"status": "failure", "data": serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)



# -----------------------------------------------------------------------------------------------------------------------------

# POLYMORPHIC SETUP - INVOICE UPLOAD

# -----------------------------------------------------------------------------------------------------------------------------


class InvoiceUploadCreateApiView(ListCreateAPIView):
    queryset = Invoiceuploads.objects.all()
    serializer_class = InvoiceUploadserializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = Invoiceuploads.objects.all()
        serializer = InvoiceUploadlistserializer(queryset, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        serializer = InvoiceUploadserializer(data=request.data)
        if serializer.is_valid():
            serializer.save(event_user = user , to_party = user.party , from_party = user.party )
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "failure", "data": serializer.errors})


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
        return Response({"status": "failure", "data": serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)



# -----------------------------------------------------------------------------------------------------------------------------------------

# MESSAGE BOX FOR WORK_EVENTS

# -----------------------------------------------------------------------------------------------------------------------------------------

class InboxListApiview(APIView):
    permission_classes = [IsAuthenticated]


    def get_queryset(self,request):
        queryset = workevents.objects.all()
        user = self.request.user
        record_type = request.GET.get("record_type","")
        if record_type == "PROGRAM":
            if user.party.party_type == "BANK":
                queryset = workevents.objects.filter(
                    to_party__name__contains=user.party.name,final="YES", type=record_type).exclude(from_state='DRAFT').order_by('created_date')
            elif user.party.party_type == "CUSTOMER":
                queryset = workevents.objects.filter(
                    to_party__name__contains= user.party.name,workitems__user__id=str(user.id), c_final="YES", type=record_type).exclude(from_state='DRAFT').order_by('created_date')
            else:
                queryset = workevents.objects.filter(
                    to_party__name__contains=self.request.user.party.name,workitems__user__id=str(user.id),c_final="YES", type="PROGRAM").exclude(from_state='DRAFT').order_by('created_date')

        if record_type == "INVOICE":
            if user.party.party_type == "BANK":
                queryset = workevents.objects.filter(
                    to_party__name__contains=user.party.name, final="YES", type="INVOICE").exclude(from_state='DRAFT').order_by('created_date')
            elif user.party.party_type == "CUSTOMER":
                queryset = workevents.objects.filter(
                    to_party__name__contains=user.party.name, c_final="YES", type="INVOICE").exclude(from_state='DRAFT').order_by('created_date')
            else:
                queryset = workevents.objects.filter(
                    to_party__name__contains=user.party.name, c_final = "YES",type="INVOICE").order_by('created_date')

        if record_type == "INVOICE_UPLOAD":
            if user.party.party_type == "BANK":
                queryset = workevents.objects.filter(
                    to_party__name__contains=user.party.name, final="YES", type="UPLOAD").exclude(from_state='DRAFT').order_by('created_date')
            elif user.party.party_type == "CUSTOMER":
                queryset = workevents.objects.filter(
                    to_party__name__contains=user.party.name, c_final="YES", type="UPLOAD").exclude(from_state='DRAFT').order_by('created_date')
            else:
                queryset = workevents.objects.filter(
                    to_party__name__contains=user.party.name, type="UPLOAD").exclude(from_state='DRAFT').order_by('created_date')
        return queryset


    def get(self, request, *args, **kwargs):
        datas = self.get_queryset(request)
        serializer = Workeventsmessageserializer(datas, many=True)
        return Response({"status": "success", "data": serializer.data},status=status.HTTP_200_OK)


class SentListApiview(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self,request):
        queryset = workevents.objects.all()
        user = self.request.user
        record_type = request.GET.get("record_type","")
        if record_type == "PROGRAM":
            queryset = workevents.objects.filter(from_party__name__contains=user.party.name, type = 'PROGRAM').exclude(from_state='DRAFT').order_by('created_date')

        elif record_type == "INVOICE":
            queryset = workevents.objects.filter(from_party__name__contains=user.party.name , type = 'INVOICE').exclude(from_state='DRAFT').order_by('created_date')

        elif record_type == "INVOICE_UPLOAD":
            queryset = workevents.objects.filter(from_party__name__contains=user.party.name , type = 'UPLOAD').exclude(from_state='DRAFT').order_by('created_date')
        
        else:
            queryset = workevents.objects.filter(from_party__name__contains=user.party.name).exclude(from_state='DRAFT').order_by('created_date')

        return queryset

    
    def list(self, request, *args, **kwargs):
        var = self.get_queryset(request)
        serializer = Workeventsmessageserializer(var, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class DraftListApiview(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self,request):
        queryset = workevents.objects.all()
        data1 = request.GET.get("current_state","")
        data2 = request.GET.get("not_current_state","")
        if data1 == "DRAFT":
            queryset = workevents.objects.filter(to_party__name__contains=self.request.user.party.name, from_state='DRAFT').order_by('created_date')
        if data2 == "DRAFT":
            queryset = workevents.objects.filter(to_party__name__contains=self.request.user.party.name,).exclude(from_state='DRAFT').order_by('created_date')
        return queryset


    def list(self, request, *args, **kwargs):
        var = self.get_queryset(request)
        serializer = Workeventsmessageserializer(var, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)



# TEST API VIEW 
class TestApiview(APIView):
    # permission_classes = [IsAuthenticated & Ismaker | IsAuthenticated & Is_administrator]
    permission_classes = [IsAuthenticated]

    # def get(self, request,pk,*args,**kwargs ):
    #     obj = generics.get_object_or_404(Programs, id=pk)
    #     # print(obj.initial_state)
    #     # li = []
    #     # cc = obj.workflowevent.last()
    #     # print(cc.user.phone)
    #     cs = obj.workflowitems.workflowevent.last()
    #     qs = workevents.objects.all().filter(type = "PROGRAM")
    #     print(qs)
    #     return Response({"status": "success", "data": "ok"}, status=status.HTTP_200_OK)

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        # print(obj)
        # ob = Parties.objects.get(id = 3)
        user = Pairings.objects.filter(program_id = 1)
        print(user)
        print("anand")
        # print(ob.pairings.total_limit)
        
        # queryset = Invoiceuploads.objects.get(id = 3)
    
        # for i in queryset.invoices:
        #     cs = Invoices.objects.create(program_type = queryset.program_type , finance_currency_type = gets(i['financing_currency']) ,party = party_types(i['buyer_name']) )
        #     print(cs)
        #     # print(type(i['buyer_name']))
        #     print(len(queryset.invoices))
        # qs = userprocessauth.objects.get(user = user)
        # print(qs.user.party.customer_id) 
        # my object for the party user related 
        return Response({"status": "success"}, status=status.HTTP_200_OK)





# PAIRING CREATE API VIEW

class PairingApiview(APIView):
    queryset = Pairings.objects.all()
    serializer_class = PairingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PairingSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"Status": "Failed", "data": serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def get_queryset(self,request):
        user = self.request.user
        data = self.request.query_params.get('pg_id')
        if data is not None:
            qs = Pairings.objects.filter(program_id = data)
        else:
            qs = Pairings.objects.filter(counterparty_id = user.party.id )
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
        return Response({"status": "failure", "data": serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)


# COUNTER PARTY API VIEW

class CounterPartyApiview(APIView):
    queryset = Parties.objects.all()
    serializer_class = CounterPartySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Parties.objects.filter(party_type = "SELLER").all()
        ser = CounterPartyListSerializer(queryset, many=True)
        return Response({"Status": "Success","data": ser.data}, status=status.HTTP_201_CREATED)

    def post(self, request):
        serializer = CounterPartySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Status": "Success",}, status=status.HTTP_201_CREATED)
        return Response({"Status": "Failed", "data": serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)


