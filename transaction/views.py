from django.contrib.admin.views.decorators import staff_member_required
from accounts.models import signatures, userprocessauth
from transaction.FSM.program import WorkFlow
from .models import (
    Actions,
    Programs, 
    submodels, 
    workevents, 
    workflowitems
)
from django.shortcuts import render
from rest_framework.exceptions import APIException, PermissionDenied
from rest_framework import serializers
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView
)
from transaction.states import StateChoices
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .serializer import (
    Actionserializer,
    Modelserializer,
    ProgramListserializer,
    Programcreateserializer,
    Workeventsmessageserializer,
    Workeventsserializer,
    Workitemserializer,
)
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import generics
from accounts.serializer import GetUserSerilaizer, signaturesserializer


User = get_user_model()

# -----------------------------------------------------------------------------------------------------------------------------

# POLYMORPHIC SETUP - PROGRAM'S

# -----------------------------------------------------------------------------------------------------------------------------


class ProgramListApiView(ListAPIView):
    queryset = Programs.objects.all()
    serializer_class = ProgramListserializer
    permission_classes = [IsAuthenticated]

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


# -------------------------------------------------------------------------------------------------

## SUBMIT TRANSITIONS 
# --------------------------------------------------------------------------------------------------


# INITIAL SUBMIT TRANSITION 

class SubmitTransitionApiView(CreateAPIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        flow = WorkFlow(obj)
        flow.submit()
        obj.save()
        return Response({"status":"success","data":"DRAFT -> SUBMIT"})



# UPDATE SIGN_A SUBMIT TRANSITION -  anand 24 jan

class SubmitTransitionSign_AApiview(CreateAPIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user
        qs = userprocessauth.objects.get(action = 'SUBMIT', model_id = 'PROGRAM')
        if (user.is_sign_a | user.is_administrator == True):
            qs_type = qs.signature.sign_a 
            if qs_type == True:
                flow = WorkFlow(obj)
                flow.submit_level_1()
                qs.sign_a = True
                qs.save()
                # obj.next_available_transitions = [StateChoices.STATUS_AW_APPROVAL]
                obj.save()
                return Response({"status":"success","data":"sign_a transition done"})
            else:
                return Response({"data":"can't do this transition"})
        return Response({"status":"failure","data":"can't do this transition"})



# UPDATE SIGN_B SUBMIT TRANSITION 

class SubmitTransitionSign_BApiview(CreateAPIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user
        qs = userprocessauth.objects.get(action = 'SUBMIT', model_id = 'PROGRAM')
        if(user.is_sign_b | user.is_administrator == True):
            qs_type = qs.signature.sign_b 
            if qs_type == True:
                flow = WorkFlow(obj)
                flow.submit_level_2()
                qs.sign_b = True
                qs.save()
                # obj.next_available_transitions = [StateChoices.STATUS_AW_APPROVAL]
                obj.save()
                return Response({"status":"success","data":"sign_B transition done"})
            else:
                return Response({"data":"can't do this transition"})
        return Response({"status":"failure","data":"can't do this transition"})


# UPDATE SIGN_C SUBMIT TRANSITION 

class SubmitTransitionSign_CApiview(CreateAPIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user
        qs = userprocessauth.objects.get(action = 'SUBMIT', model_id = 'PROGRAM')
        if(user.is_sign_c | user.is_administrator == True):
            qs_type = qs.signature.sign_c
            if qs_type == True:
                flow = WorkFlow(obj)
                flow.submit_level_3()
                qs.sign_c = True
                qs.save()
                # obj.next_available_transitions = [StateChoices.STATUS_AW_APPROVAL]
                obj.save()
                return Response({"status":"success","data":"sign_C transition done"})
            else:
                return Response({"data":"can't do this transition"})
        return Response({"status":"failure","data":"can't do this transition"})


# -------------------------------------------------------------------------------------------------

## REJECT TRANSITIONS 
# --------------------------------------------------------------------------------------------------

# INITIAL REJECT TRANSITION

class RejectTransitionApiView(CreateAPIView):
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


# --------------------------------------------------------------------------------------------------------------------

## ACCEPT TRANSITIONS
# --------------------------------------------------------------------------------------------------------------------


# INITIAL ACCEPT TRANSIION 


class AcceptTransitionApiview(ListAPIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        flow = WorkFlow(obj)
        flow.accept()
        obj.save()
        return Response({"data":"Success"})


# ACCEPT SIGN_A TRANSITION API VIEW

class AcceptSign_AApiView(ListAPIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        flow = WorkFlow(obj)
        flow.accept_level_1()
        obj.save()
        return Response({"data":"Success","action":"from draft  -> sign_a"})


# ACCEPT SIGN_B TRANSITION API VIEW

class AcceptSign_BApiView(ListAPIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        flow = WorkFlow(obj)
        flow.accept_level_2()
        obj.save()
        return Response({"data":"success","action":"from aw_ap  -> sign_b"})


# ACCEPT SIGN_C TRANSITION API VIEW

class AcceptSign_CApiView(ListAPIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        flow = WorkFlow(obj)
        flow.accept_level_3()
        obj.save()
        return Response({"data":"success","action":"from aw_ap  -> sign_c"})
    


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


# TEST API VIEW
class TestApiview(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        print(obj.next_available_transitions)   
        return Response({"status": "success", "data": "ok"},status=status.HTTP_200_OK)

