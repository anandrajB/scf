from accounts.models import Parties, userprocessauth
from .models import (
    Invoices,
    Pairings,
    Programs,
    workevents,
)
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
    PairingSerializer,
    ProgramListserializer,
    Programcreateserializer,
    Workeventsmessageserializer,
    Workeventsserializer,
)
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import generics
from .permission.program_permission import Ismaker

User = get_user_model()

# -----------------------------------------------------------------------------------------------------------------------------

# POLYMORPHIC SETUP - PROGRAM'S

# -----------------------------------------------------------------------------------------------------------------------------


class ProgramListApiView(ListAPIView):
    queryset = Programs.objects.all()
    serializer_class = ProgramListserializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.party.party_type == "BANK" and user.is_administrator == True:
            queryset = Programs.objects.all()
        else:
            queryset = Programs.objects.filter(party=user.party)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProgramListserializer(queryset,many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class ProgramCreateApiView(APIView):
    queryset = Programs.objects.all()
    serializer_class = Programcreateserializer
    permission_classes = [Ismaker]

    def post(self, request):
        serializer = Programcreateserializer(data=request.data)
        if serializer.is_valid():
            serializer.save(event_user = request.user)
            return Response({"status": "success"}, status=status.HTTP_201_CREATED)
        return Response({"status": "failure", "data": serializer.errors})


class ProgramUpdateDeleteApiview(RetrieveUpdateDestroyAPIView):
    queryset = Programs.objects.all()
    serializer_class = ProgramListserializer
    permission_classes = [IsAuthenticated]
    # metadata_class = APIRootMetadata

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
        return Response({"status": "failure", "data": serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)


class WorkEventCreateApiview(CreateAPIView):
    queryset = workevents.objects.all()
    serializer_class = Workeventsserializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = Workeventsserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success"}, status=status.HTTP_201_CREATED)
        return Response({"status": "failure", "data": serializer.errors}, status=status.HTTP_424_FAILED_DEPENDENCY)



# -----------------------------------------------------------------------------------------------------------------------------

# POLYMORPHIC SETUP - INVOICE'S

# -----------------------------------------------------------------------------------------------------------------------------


class InvoiceListApiView(ListAPIView):
    queryset = Invoices.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.party.party_type == "BANK":
            queryset = Invoices.objects.all()
        else:
            queryset = Invoices.objects.all()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = Invoices.objects.all()
        serializer = InvoiceSerializer(queryset, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class InvoiceCreateApiView(APIView):
    queryset = Invoices.objects.all()
    serializer_class = InvoiceCreateserializer
    permission_classes = [Ismaker]

    def post(self, request):
        serializer = InvoiceCreateserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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


# -----------------------------------------------------------------------------------------------------------------------------------------

# MESSAGE BOX FOR WORK_EVENTS

# -----------------------------------------------------------------------------------------------------------------------------------------

class InboxListApiview(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.party.party_type == "BANK":
            queryset = workevents.objects.all().filter(final='YES')
            print("bank final")
        elif user.party.party_type == "CUSTOMER":
            queryset = workevents.objects.all().filter(c_final='YES')
            print("customer final")
        else:
            queryset = workevents.objects.filter(
                to_party__name__contains=self.request.user.party.name).exclude(from_state='DRAFT')
        return queryset

    def list(self, request, *args, **kwargs):
        var = self.get_queryset()
        serializer = Workeventsmessageserializer(var, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class SentListApiview(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = workevents.objects.filter(
            from_party__name__contains=self.request.user.party.name).exclude(from_state='DRAFT')
        return queryset

    def list(self, request, *args, **kwargs):
        var = self.get_queryset()
        serializer = Workeventsmessageserializer(var, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class DraftListApiview(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = workevents.objects.filter(
            from_party__name__contains=self.request.user.party.name, from_state='DRAFT')
        return queryset

    def list(self, request, *args, **kwargs):
        var = self.get_queryset()
        serializer = Workeventsmessageserializer(var, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)



def current(request):
    return request.user



# TEST API VIEW 
class TestApiview(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        bank = Parties.objects.get(party_type = "BANK")
        user = self.request.user.party
        print("tghe name" ,user)
        # print(obj
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
