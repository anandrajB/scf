from django.contrib.admin.views.decorators import staff_member_required
from accounts.models import signatures
from .models import Programs, workevents, workflowitems
from django.shortcuts import render
from rest_framework.exceptions import APIException, PermissionDenied
from django_fsm import has_transition_perm, get_available_FIELD_transitions
from rest_framework import serializers
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView
)
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .serializer import (
    ProgramListserializer,
    Programcreateserializer,
    Workeventsserializer,
)
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import generics
from accounts.serializer import signaturesserializer


User = get_user_model()

# -----------------------------------------------------------------------------

# POLYMORPHIC SETUP - PROGRAM'S

# -----------------------------------------------------------------------------


class ProgramListApiView(ListAPIView):
    queryset = Programs.objects.all()
    serializer_class = ProgramListserializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProgramListserializer(queryset, many=True)
        return Response({"status": "success", "data": serializer.data},status=status.HTTP_200_OK)


class ProgramCreateApiView(CreateAPIView):
    queryset = Programs.objects.all()
    serializer_class = Programcreateserializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = Programcreateserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success"}, status=status.HTTP_201_CREATED)
        return Response({"status": "failure", "data": serializer.errors})


class ProgramUpdateDeleteApiview(RetrieveUpdateDestroyAPIView):
    queryset = Programs.objects.all()
    serializer_class = ProgramListserializer
    permission_classes = [AllowAny]
    # metadata_class = APIRootMetadata

    def retrieve(self, request, pk=None):
        queryset = Programs.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ProgramListserializer(user)
        return Response({"status": "success", "data": serializer.data},status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        queryset = Programs.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ProgramListserializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data},status=status.HTTP_200_OK)
        return Response({"status": "failure", "data": serializer.errors},status=status.HTTP_406_NOT_ACCEPTABLE)


class WorkEventCreateApiview(CreateAPIView):
    queryset = workevents.objects.all()
    serializer_class = Workeventsserializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = Workeventsserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success"}, status=status.HTTP_201_CREATED)
        return Response({"status": "failure", "data": serializer.errors},status=status.HTTP_424_FAILED_DEPENDENCY)


class SignatureList(ListAPIView):
    queryset = signatures.objects.all()
    serializer_class = signaturesserializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = signatures.objects.all()
        serializer = signaturesserializer(queryset, many=True)
        return Response({"status": "success", "data": serializer.data},status=status.HTTP_200_OK)


# -----------------------------------------------------------------------------

# MESSAGE BOX FOR WORK_EVENTS

# -----------------------------------------------------------------------------

class InboxListApiview(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = workevents.objects.filter(
            to_party__name__contains=self.request.user.parties.name).exclude(from_state='DRAFT')
        return queryset

    def list(self, request, *args, **kwargs):
        var = self.get_queryset()
        serializer = Workeventsserializer(var, many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)


class SentListApiview(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = workevents.objects.filter(
            from_party__name__contains=self.request.user.parties.name).exclude(from_state='DRAFT')
        return queryset

    def list(self, request, *args, **kwargs):
        var = self.get_queryset()
        serializer = Workeventsserializer(var, many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)



class DraftListApiview(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # print(self.request.user.parties.name)
        queryset = workevents.objects.filter(
            from_party__name__contains=self.request.user.parties.name, from_state='DRAFT')
        return queryset

    def list(self, request, *args, **kwargs):
        var = self.get_queryset()
        serializer = Workeventsserializer(var, many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)


# -----------------------------------------------------------------------------

# FSM TRANSITION FUNCTIONS ----

# -----------------------------------------------------------------------------

# SUBMIT /--  ACTION

@api_view(['GET', 'POST'])
def deleted(self, pk):
    obj = generics.get_object_or_404(workflowitems, id=pk)
    obj.delete()
    obj.save()
    return "data ok "


@api_view(['POST','PATCH'])
def submitted(self, pk):
    # if workflowitems.objects.get(id=pk , initial_state = 'DELETED' ):
    #     raise APIException({"YOUR SUBMISION IS ALREADY DELETED , PLEASE CHECK "})
    obj = generics.get_object_or_404(workflowitems, id=pk)
    obj.submit()
    obj.save()
    return Response(" submit success ")


@api_view(['GET', 'PATCH'])
def submitted_level_1(request, pk):
    try:
        workflowitems.objects.get(id=pk, initial_state='DRAFT')
        return APIException({"status : not ok"})
    except:
        obj = generics.get_object_or_404(workflowitems, id=pk)
        if not has_transition_perm(obj.submit_sign_a, request.user):
            raise PermissionDenied
        obj.submit_sign_a()
        obj.save()
        transitions = list(obj.get_available_FIELD_transitions())
        print(transitions)
        return Response({"Sign_A => Approval Awaited"})


@api_view(['GET', 'PATCH'])
def submitted_level_2(self, pk):
    obj = generics.get_object_or_404(workflowitems, id=pk)
    obj.submit_sign_b()
    obj.save()
    transitions = list(obj.get_available_FIELD_transitions())
    print(transitions)
    return Response("Sign_B => Approval Awaited")


@api_view(['GET', 'PATCH'])
def submitted_level_3(self, pk):
    obj = generics.get_object_or_404(workflowitems, id=pk)
    obj.submit_sign_c()
    obj.save()
    transitions = list(obj.get_available_FIELD_transitions())
    print(transitions)
    return Response("Sign_C => Approval Awaited")


@api_view(['GET', 'PATCH'])
def submit_rejected(self, pk):
    obj = generics.get_object_or_404(workflowitems, id=pk)
    obj.submit_reject()
    obj.save()
    transitions = list(obj.get_available_FIELD_transitions())
    print(transitions)
    return Response("submission rejected")


# REJECT WORKFLOW 12/2021

# class WorkeventRejectapiview(RetrieveUpdateAPIView):
#     queryset = Programs.objects.all()
#     serializer_class = ProgramListserializer


#     def update(self, request, pk=None):
#         queryset = Programs.objects.all()
#         useraa = get_object_or_404(queryset, pk=pk)
#         print(useraa.workflowitem.id)
#         serializer = signaturesserializer(useraa, data=request.data)
#         if serializer.is_valid():
#             serializer.save(sign_c = True)
#             obj = generics.get_object_or_404(workflowitems, id=useraa.workflowitem.id)
#             obj.submit_sign_c()
#             obj.save()
#             # print(self.workflowitem)
#             return Response({"status": "ok", "data": serializer.data})
#         return Response({"status": "no "})
