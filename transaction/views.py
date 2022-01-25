from django.contrib.admin.views.decorators import staff_member_required
from accounts.models import signatures, userprocessauth
from transaction.flows import WorkFlow
from .models import (
    Actions,
    Programs, 
    submodels, 
    workevents, 
    workflowitems
)
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
    Actionserializer,
    Modelserializer,
    ProgramListserializer,
    Programcreateserializer,
    Workeventsserializer,
    Workitemserializer,
)
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import generics
from accounts.serializer import signaturesserializer


User = get_user_model()

# -----------------------------------------------------------------------------------------------------------------------------

# POLYMORPHIC SETUP - PROGRAM'S

# -----------------------------------------------------------------------------------------------------------------------------


class ProgramListApiView(ListAPIView):
    queryset = Programs.objects.all()
    serializer_class = ProgramListserializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProgramListserializer(queryset, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


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
        print(user.workflowitems.workflowevent)
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




# -----------------------------------------------------------------------------------------------------------------------------------------

# MESSAGE BOX FOR WORK_EVENTS

# -----------------------------------------------------------------------------------------------------------------------------------------

class InboxListApiview(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = workevents.objects.filter(
            to_party__name__contains=self.request.user.party.name).exclude(from_state='DRAFT')
        return queryset

    def list(self, request, *args, **kwargs):
        var = self.get_queryset()
        serializer = Workeventsserializer(var, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class SentListApiview(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = workevents.objects.filter(
            from_party__name__contains=self.request.user.party.name).exclude(from_state='DRAFT')
        return queryset

    def list(self, request, *args, **kwargs):
        var = self.get_queryset()
        serializer = Workeventsserializer(var, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class DraftListApiview(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = workevents.objects.filter(
            from_party__name__contains=self.request.user.party.name, from_state='DRAFT')
        return queryset

    def list(self, request, *args, **kwargs):
        var = self.get_queryset()
        serializer = Workeventsserializer(var, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


# -----------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------

# API FOR TRANSITION'S

# -----------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------


# DELETE TRANSITION VIEW

class TransitionDeleteApiview(CreateAPIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        flow = WorkFlow(obj)
        flow.delete()
        print("submitted success")
        obj.save()
        return Response({"data": "Success", "action": "SUBMIT"})


# INITIAL SUBMIT TRANSITION 

class SubmitTransitionApiView(CreateAPIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        flow = WorkFlow(obj)
        flow.submit()
        print("submitted success")
        obj.save()
        return Response({"data": "Success", "action": "SUBMIT"})




# UPDATE SIGN_A SUBMIT TRANSITION -  anand 24 jan

class SubmitTransitionSign_AApiview(CreateAPIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        if (obj.sign.type == 1) or (obj.sign.type == 2 ) or (obj.sign.type == 3):
            try:
                aa = signatures.objects.get(id = obj.sign.id)
                aa.sign_a = True
                aa.save()
                
            except:
                return Response({"no record found"})
            flow = WorkFlow(obj)
            flow.submit_level_1()
            obj.save()
            return Response({"ok changed -> sign_a "})
        else:
            return Response({"can't do "})



# UPDATE SIGN_B SUBMIT TRANSITION 

class SubmitTransitionSign_BApiview(CreateAPIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        if (obj.sign.type == 2) or (obj.sign.type ==3) :
            try:
                aa = signatures.objects.get(id = obj.sign.id)
                aa.sign_b = True
                aa.save()
                
            except:
                return Response({"no record found"})
            flow = WorkFlow(obj)
            flow.submit_level_2()
            obj.save()
            return Response({"ok changed -> sign_b "})
        else:
            return Response({"can't do this transition "})


# UPDATE SIGN_C SUBMIT TRANSITION 

class SubmitTransitionSign_CApiview(CreateAPIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        if (obj.sign.type == 3):
            try:
                aa = signatures.objects.get(id = obj.sign.id)
                aa.sign_c = True
                aa.save()
                
            except:
                return Response({"no record found"})
            flow = WorkFlow(obj)
            flow.submit_level_3()
            obj.save()
            return Response({"ok changed "})
        else:
            return Response({"can't do this transition  "})


# -----------------------------------------------------------------------------

## REJECT TRANSITIONS 
# -----------------------------------------------------------------------------

# REJECT TRANSITION

class RejectedSignApi(CreateAPIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        flow = WorkFlow(obj)
        flow.reject()
        obj.save()
        return Response({"ok changed => reject"})
        

# REJECT SIGN_A TRANSITION

class RejectSign_AApiview(CreateAPIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        qss = signatures.objects.get(action = 'REJECT',user = request.user.id )
        obj.sign.id = qss
        print(qss.type)
        print("changed")
        if (qss.type == 1) or (qss.type == 2) or (qss.type == 3):
            try:
                aa = signatures.objects.get(id = qss.id)
                aa.sign_a = True
                aa.save()
            except:
                return Response({"no record found"})
            flow = WorkFlow(obj)
            flow.reject_level_1()
            obj.save()
            return Response({"ok changed "})
        else:
            return Response({"can't do this transition "})



# REJECT SIGN_B TRANSITION 


class RejectSign_BApiview(CreateAPIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        qss = signatures.objects.get(action = 'REJECT',user = request.user.id )
        obj.sign.id = qss
        print(qss.type)
        if (qss.type == 2) or (qss.type ==3) :
            try:
                aa = signatures.objects.get(id = qss.id)
                aa.sign_b = True
                aa.save()
                
            except:
                return Response({"no record found"})
            flow = WorkFlow(obj)
            flow.reject_level_2()
            obj.save()
            return Response({"ok changed "})
        else:
            return Response({"can't do this transition  "})


# REJECT SIGN_C TRANSITION

class RejectSign_CApiview(CreateAPIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        qss = signatures.objects.get(action = 'REJECT',user = request.user.id )
        # print(qss)
        obj.sign.id = qss
        # print(obj.sign_id)
        print("the type is ", qss.type)
        if (qss.type == 3):
            try:
                aa = signatures.objects.get(id = qss.id)
                aa.sign_c = True
                aa.save()
                
            except:
                return Response({"no record found"})
            flow = WorkFlow(obj)
            flow.reject_level_3()
            obj.save()
            return Response({"ok changed "})
        else:
            return Response({"can't do this transition  "})


# -----------------------------------------------------------------------------

## ACCEPT TRANSITIONS
# -----------------------------------------------------------------------------


@api_view(['GET', 'PATCH'])
def accepted(request, pk):
    obj = generics.get_object_or_404(workflowitems, id=pk)
    flow = WorkFlow(obj)
    flow.accept()
    print("Step changed")
    obj.save()
    return Response({"data": "Success", "action": "ACCEPT"})


@api_view(['GET', 'PATCH'])
def accepted_1(request, pk):
    obj = generics.get_object_or_404(workflowitems, id=pk)
    flow = WorkFlow(obj)
    flow.accept_level_1()
    print("Step changed")
    obj.save()
    return Response({"data": "Success", "action": "ACCEPT"})


@api_view(['GET', 'PATCH'])
def accepted_2(request, pk):
    obj = generics.get_object_or_404(workflowitems, id=pk)
    flow = WorkFlow(obj)
    flow.accept_level_2()
    print("Step changed")
    obj.save()
    return Response({"data": "Success", "action": "ACCEPT"})


@api_view(['GET', 'PATCH'])
def accepted_3(request, pk):
    obj = generics.get_object_or_404(workflowitems, id=pk)
    flow = WorkFlow(obj)
    flow.accept_level_3()
    print("Step changed")
    obj.save()
    return Response({"data": "Success", "action": "ACCEPT"})
    

# -----------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------

# END OF TRANSITION API'S

# -----------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------




# SUBMODEL CREATE API VIEW

class ModelCreateApiview(ListCreateAPIView):
    queryset = submodels.objects.all()
    serializer_class = Modelserializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = Modelserializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response({"Status": "Success"},status=status.HTTP_201_CREATED)
        return Response({"Status": "Failed", "data": serializer.errors},status=status.HTTP_406_NOT_ACCEPTABLE)

    def list(self, request):
        model1 = submodels.objects.all()
        serializer = Modelserializer(model1, many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)


# ACTION CREATE API 

class ActionCreateApiView(ListCreateAPIView):
    queryset = Actions.objects.all()
    serializer_class = Actionserializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = Actionserializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response({"Status": "Success"},status=status.HTTP_201_CREATED)
        return Response({"Status": "Failed", "data": serializer.errors},status=status.HTTP_406_NOT_ACCEPTABLE)

    def list(self, request):
        model1 = Actions.objects.all()
        serializer = Actionserializer(model1, many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)


