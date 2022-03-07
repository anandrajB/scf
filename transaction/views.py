from urllib.request import Request
from django.http import Http404
from accounts.models import Parties, signatures, userprocessauth
from accounts.permission import Is_Administrator
from transaction.permission.upload_permissions import Ismaker_upload
from rest_framework.viewsets import GenericViewSet
from .models import (
    Invoices,
    Invoiceuploads,
    Pairings,
    Programs,
    Transitionpartytype,
    workevents,
    workflowitems,
)
from transaction.permission.program_permission import *
from transaction.permission.upload_permissions import *
from django.shortcuts import render
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .serializer import (
    InvoiceCreateserializer,
    InvoiceSerializer,
    InvoiceUploadlistserializer,
    InvoiceUploadserializer,
    PairingSerializer,
    ProgramListserializer,
    ProgramMetaData,
    Programcreateserializer,
    Workeventsmessageserializer,
    Workeventsserializer,
    programupdateserilizer
)
from rest_framework.decorators import api_view, permission_classes, renderer_classes
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
    permission_classes = [IsAuthenticated & Ismaker | IsAuthenticated & Is_Administrator]

    def get_queryset(self):
        user = self.request.user
        if user.is_administrator == True:
            queryset = Programs.objects.all()
        else:
            queryset = Programs.objects.filter(party=user.party)
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProgramListserializer(queryset,many=True)
        qs = ProgramMetaData(queryset , many = True)
        return Response({"status": "success","data": serializer.data}, status=status.HTTP_200_OK)


    def post(self, request):
        user = request.user
        serializer = Programcreateserializer(data=request.data)
        if serializer.is_valid():
            serializer.save(from_party = user.party,to_party = user.party,event_user = user)
            return Response({"status": "success"}, status=status.HTTP_201_CREATED)
        return Response({"status": "failure", "data": serializer.errors})



class ProgramUpdateDeleteApiview(APIView):
    serializer_class = programupdateserilizer
    # permission_classes = [IsAuthenticated]
    # metadata_class = APIRootMetadata

    def get(self, request, pk=None):
        queryset = Programs.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ProgramListserializer(user)
        metadata = ProgramMetaData(user)
        return Response({"status": "success","metadata": metadata.data,"data": serializer.data}, status=status.HTTP_200_OK)

    # def get_object(self, pk):
    #     try:
    #         return Programs.objects.get(pk=pk)
    #     except Programs.DoesNotExist:
    #         raise Http404

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
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk, format=None):
    #     program = get_object_or_404(pk=pk)
    #     program.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


# -----------------------------------------------------------------------------------------------------------------------------

# POLYMORPHIC SETUP - INVOICE'S (manual create)

# -----------------------------------------------------------------------------------------------------------------------------


class InvoiceCreateApiView(ListCreateAPIView):
    queryset = Invoices.objects.all()
    serializer_class = InvoiceCreateserializer
    permission_classes = [IsAuthenticated,Ismaker]

    def get_queryset(self):
        user = self.request.user
        if user.is_administrator == True:
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
            return Response({"status": "success"}, status=status.HTTP_201_CREATED)
        return Response({"status": "failure", "data": serializer.errors})


class InvoiceUpdateDeleteApiview(RetrieveUpdateDestroyAPIView):
    queryset = Invoices.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]
    # metadata_class = APIRootMetadata

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


class InvoiceUploadListapiview(ListAPIView):
    queryset = Invoiceuploads.objects.all()
    serializer_class = InvoiceUploadlistserializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_administrator == True:
            queryset = Invoiceuploads.objects.all()
        else:
            queryset = Invoiceuploads.objects.all()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = Invoiceuploads.objects.all()
        serializer = InvoiceUploadlistserializer(queryset, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class InvoiceUploadCreateApiView(GenericViewSet):
    queryset = Invoiceuploads.objects.all()
    serializer_class = InvoiceUploadserializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = Invoiceuploads.objects.all()
        serializer = InvoiceUploadlistserializer(queryset, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        user = request.user
        is_many = isinstance(request.data, list)
        if not is_many:
            serializer = InvoiceUploadserializer(data=request.data)
            if serializer.is_valid():
                serializer.save(from_party = user.party,to_party = user.party,event_user = user)
                return Response({"status": "success"}, status=status.HTTP_201_CREATED)
            return Response({"status": "failure", "data": serializer.errors})
        else:
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            # self.perform_create(serializer)
            serializer.save(from_party = user.party,to_party = user.party,event_user = user)
            # headers = self.get_success_headers(serializer.data)
            return Response({"status": "success"}, status=status.HTTP_201_CREATED)


class InvoiceUploadUpdateDeleteApiview(RetrieveUpdateDestroyAPIView):
    queryset = Invoiceuploads.objects.all()
    serializer_class = InvoiceUploadlistserializer
    permission_classes = [IsAuthenticated]
    # metadata_class = APIRootMetadata

    def retrieve(self, request, pk=None):
        queryset = Invoiceuploads.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        print(user.invoices['due_date'])
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
    # serializer_class = Workeventsmessageserializer

    def get_queryset(self,request):
        queryset = workevents.objects.all()
        user = self.request.user
        record_type = request.GET.get("record_type","")
        print(record_type)
        if record_type == "PROGRAM":
            if user.is_administrator == True:
                queryset = workevents.objects.filter(
                    to_party__name__contains=self.request.user.party.name, final="YES", type=record_type).exclude(from_state='DRAFT').order_by('created_date')
            elif user.party.party_type == "CUSTOMER":
                queryset = workevents.objects.filter(
                    to_party__name__contains=self.request.user.party.name, c_final="YES", type="PROGRAM").exclude(from_state='DRAFT').order_by('created_date')
            else:
                queryset = workevents.objects.filter(
                    to_party__name__contains=self.request.user.party.name, type="PROGRAM").exclude(from_state='DRAFT').order_by('created_date')

        if record_type == "INVOICE":
            if user.is_administrator == True:
                queryset = workevents.objects.filter(
                    to_party__name__contains=self.request.user.party.name, final="YES", type="INVOICE").exclude(from_state='DRAFT').order_by('created_date')
            elif user.party.party_type == "CUSTOMER":
                queryset = workevents.objects.filter(
                    to_party__name__contains=self.request.user.party.name, c_final="YES", type="INVOICE").exclude(from_state='DRAFT').order_by('created_date')
            
            else:
                queryset = workevents.objects.filter(
                    to_party__name__contains=self.request.user.party.name, type="INVOICE").exclude(from_state='DRAFT').order_by('created_date')

        if record_type == "INVOICE_UPLOAD":
            if user.is_administrator == True:
                queryset = workevents.objects.filter(
                    to_party__name__contains=self.request.user.party.name, final="YES", type="UPLOAD").exclude(from_state='DRAFT').order_by('created_date')
            elif user.party.party_type == "CUSTOMER":
                queryset = workevents.objects.filter(
                    to_party__name__contains=self.request.user.party.name, c_final="YES", type="UPLOAD").exclude(from_state='DRAFT').order_by('created_date')
            
            else:
                queryset = workevents.objects.filter(
                    to_party__name__contains=self.request.user.party.name, type="UPLOAD").exclude(from_state='DRAFT').order_by('created_date')
        return queryset


    def get(self, request, *args, **kwargs):
        datas = self.get_queryset(request)
        serializer = Workeventsmessageserializer(datas, many=True)
        return Response(serializer.data)


class SentListApiview(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = workevents.objects.filter(
            from_party__name__contains=self.request.user.party.name).exclude(from_state='DRAFT').order_by('created_date')
        return queryset

    def list(self, request, *args, **kwargs):
        var = self.get_queryset()
        serializer = Workeventsmessageserializer(var, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class DraftListApiview(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self,request):
        queryset = workevents.objects.all()
        data1 = request.GET.get("current_state","")
        data2 = request.GET.get("not_current_state","")
        record = request.GET.get("record_type","")
        if data1 == "DRAFT":
            queryset = workevents.objects.filter(to_party__name__contains=self.request.user.party.name, from_state='DRAFT').order_by('created_date')
        if data2 == "DRAFT":
            queryset = workevents.objects.filter(to_party__name__contains=self.request.user.party.name,).exclude(from_state='DRAFT').order_by('created_date')
        # if record == "PROGRAM":
        #     queryset = workevents.objects.filter(to_party__name__contains=self.request.user.party.name,type = "PROGRAM").order_by('created_date')
        # elif record == "INVOICE":
        #     queryset = workevents.objects.filter(to_party__name__contains=self.request.user.party.name,type = "INVOICE").exclude(from_state='DRAFT').order_by('created_date')
        # if record == "INVOICE_UPLOAD":
        #      queryset = workevents.objects.filter(to_party__name__contains=self.request.user.party.name,type = "UPLOAD",from_state = 'DRAFT').order_by('created_date')
        return queryset


    def list(self, request, *args, **kwargs):
        var = self.get_queryset(request)
        serializer = Workeventsmessageserializer(var, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

# current user 
def currentuser(request):
    return request.user


def myfun(request):
    user = request.user
    bank = Parties.objects.get(party_type="BANK")
    if user.is_administrator == True:
        obj = signatures.objects.get(
                party=bank, action__desc__contains="REJECT", model="PROGRAM")
        
    else :
        obj = signatures.objects.get(
                party=user.party, action__desc__contains="REJECT", model="PROGRAM")
    
    return obj

from rest_framework.request import HttpRequest, Request
from django.http import request as RQ
@api_view(['GET'])
@permission_classes((Is_Administrator, ))
def myview(request):
    return Response({"data": {"status": "success"}})

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
        print(type(obj.id))
        # qs = userprocessauth.objects.get(user = user)
        # print(qs.user.party.customer_id) 
        # my object for the party user related 
        return Response({"status": "success", "data": "ok"}, status=status.HTTP_200_OK)





# PAIRING CREATE API VIEW

class PairingApiview(ListCreateAPIView):
    queryset = Pairings.objects.all()
    serializer_class = PairingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PairingSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response({"Status": "Success"}, status=status.HTTP_201_CREATED)
        return Response({"Status": "Failed", "data": serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def list(self, request):
        model1 = Pairings.objects.all()
        serializer = PairingSerializer(model1, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


# PAIRING UPDATE API VIEW

class PairingUpdateapiview(RetrieveUpdateDestroyAPIView):
    queryset = Pairings.objects.all()
    serializer_class = PairingSerializer
    permission_classes = [IsAuthenticated]
    # metadata_class = APIRootMetadata

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
