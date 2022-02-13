from transaction.FSM.program import WorkFlow
from accounts.models import signatures
from transaction.models import workflowitems 
from transaction.permission.program_permission import (
    Is_Accepter,
    Is_Rejecter,
    Is_administrator,
    IsAccept_Sign_A,
    IsAccept_Sign_B, 
    IsReject_Sign_A, 
    IsReject_Sign_B, 
    IsReject_Sign_C, 
    Ismaker, 
    IsSign_A , 
    IsSign_B  , 
    Is_Sign_C
)
from transaction.serializer import Workitemserializer
from rest_framework.generics import (
    ListAPIView ,
    ListCreateAPIView,
    CreateAPIView
)
from rest_framework import generics
from rest_framework.response import Response




# -----------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------

# API FOR TRANSITION'S - PROGRAM (CUSTOMER )

# -----------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------


# DELETE TRANSITION VIEW

class TransitionDeleteApiview(CreateAPIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [Ismaker]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        flow = WorkFlow(obj)
        flow.delete()
        obj.save()
        return Response({"data": "Success", "action": "SUBMIT"})


# -----------------------------------

# SUBMIT TRANSITIONS
# -----------------------------------


# INITIAL SUBMIT TRANSITION

class SubmitTransitionApiView(CreateAPIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [Ismaker]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        flow = WorkFlow(obj)
        flow.submit()
        obj.save()
        return Response({"status": "success", "data": "DRAFT -> SUBMIT"})


# UPDATE SIGN_A SUBMIT TRANSITION -  anand 24 jan

class SubmitTransitionSign_AApiview(CreateAPIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsSign_A ]
        
    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user
        party = obj.program.party
        signs = signatures.objects.get(party=party, action__desc__contains='SUBMIT', model='PROGRAM')
        if user.party == party:
            if signs.sign_a == True:
                flow = WorkFlow(obj)
                flow.submit_level_1()
                obj.save()
                return Response({"status": "success", "data": "SUBMIT : sign_A transition done"})
            else:
                return Response({"data": "can't do this transition"})
        else:
            return Response({"data":"can't do this transition "})
        


# UPDATE SIGN_B SUBMIT TRANSITION

class SubmitTransitionSign_BApiview(CreateAPIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsSign_B]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user
        party = obj.program.party
        signs = signatures.objects.get(party=party, action__desc__contains='SUBMIT', model='PROGRAM')
        if user.party == party:
            if signs.sign_b == True:
                flow = WorkFlow(obj)
                flow.submit_level_2()
                obj.save()
                return Response({"status": "success", "data": "SUBMIT : sign_B transition done"})
            else:
                return Response({"data": "can't do this transition"})
        else:
            return Response({"data":"can't do this transition "})
        

# UPDATE SIGN_C SUBMIT TRANSITION

class SubmitTransitionSign_CApiview(CreateAPIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [Is_Sign_C]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user
        party = obj.program.party
        signs = signatures.objects.get(party=party, action__desc__contains='SUBMIT', model='PROGRAM')
        if user.party == party:
            if signs.sign_c == True:
                flow = WorkFlow(obj)
                flow.submit_level_3()
                obj.save()
                return Response({"status": "success", "data": "SUBMIT : sign_C transition done"})
            else:
                return Response({"data": "can't do this transition"})
        else:
            return Response({"data":"can't do this transition "})
     


# -----------------------------------------

# REJECT TRANSITIONS
# -----------------------------------------

# INITIAL REJECT TRANSITION

class RejectTransitionApiView(CreateAPIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [Is_Rejecter]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        flow = WorkFlow(obj)
        flow.reject()
        obj.save()
        return Response({"ok changed => REJECT"})


# REJECT SIGN_A TRANSITION

class RejectSign_AApiview(CreateAPIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsReject_Sign_A]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user
        party = obj.program.party
        signs = signatures.objects.get(party=party, action__desc__contains='REJECT', model='PROGRAM')
        if user.party == party:
            if signs.sign_a == True:
                flow = WorkFlow(obj)
                flow.reject_level_1()
                obj.save()
                return Response({"status": "success", "data": "REJECT : sign_C transition done"})
            else:
                return Response({"data": "can't do this transition"})
        else:
            return Response({"data":"can't do this transition "})



# REJECT SIGN_B TRANSITION


class RejectSign_BApiview(CreateAPIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsReject_Sign_B]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user
        party = obj.program.party
        signs = signatures.objects.get(party=party, action__desc__contains='REJECT', model='PROGRAM')
        if user.party == party:
            if signs.sign_b == True:
                flow = WorkFlow(obj)
                flow.reject_level_2()
                obj.save()
                return Response({"status": "success", "data": "REJECT : sign_B transition done"})
            else:
                return Response({"data": "can't do this transition"})
        else:
            return Response({"data":"can't do this transition "})


# REJECT SIGN_C TRANSITION


class RejectSign_CApiview(CreateAPIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsReject_Sign_C]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user
        party = obj.program.party
        signs = signatures.objects.get(party=party, action__desc__contains='REJECT', model='PROGRAM')
        if user.party == party:
            if signs.sign_c == True:
                flow = WorkFlow(obj)
                flow.reject_level_3()
                obj.save()
                return Response({"status": "success", "data": "REJECT : sign_C transition done"})
            else:
                return Response({"data": "can't do this transition"})
        else:
            return Response({"data":"can't do this transition "})



# -----------------------------------------

# ACCEPT TRANSITIONS
# ----------------------------------------


# INITIAL ACCEPT TRANSIION


class AcceptTransitionApiview(ListAPIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [Is_Accepter]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        flow = WorkFlow(obj)
        flow.accept()
        obj.save()
        return Response({"status": "Success","data":"initial accept"})


# ACCEPT SIGN_A TRANSITION API VIEW

class AcceptSign_AApiView(ListAPIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAccept_Sign_A]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user
        party = obj.program.party
        signs = signatures.objects.get(party=party, action__desc__contains='ACCEPT', model='PROGRAM')
        if user.party == party:
            if signs.sign_a == True:
                flow = WorkFlow(obj)
                flow.accept_level_1()
                obj.save()
                return Response({"status": "success", "data": "ACCEPT : sign_A transition done"})
            else:
                return Response({"data": "can't do this transition"})
        else:
            return Response({"data":"can't do this transition "})

# ACCEPT SIGN_B TRANSITION API VIEW

class AcceptSign_BApiView(ListAPIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAccept_Sign_B]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user
        party = obj.program.party
        signs = signatures.objects.get(party=party, action__desc__contains='ACCEPT', model='PROGRAM')
        if user.party == party:
            if signs.sign_b == True:
                flow = WorkFlow(obj)
                flow.accept_level_2()
                obj.save()
                return Response({"status": "success", "data": "ACCEPT : sign_B transition done"})
            else:
                return Response({"data": "can't do this transition"})
        else:
            return Response({"data":"can't do this transition "})

# ACCEPT SIGN_C TRANSITION API VIEW

class AcceptSign_CApiView(ListAPIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user
        party = obj.program.party
        signs = signatures.objects.get(party=party, action__desc__contains='ACCEPT', model='PROGRAM')
        if user.party == party:
            if signs.sign_c == True:
                flow = WorkFlow(obj)
                flow.accept_level_3()
                obj.save()
                return Response({"status": "success", "data": "ACCEPT : sign_C transition done"})
            else:
                return Response({"data": "can't do this transition"})
        else:
            return Response({"data":"can't do this transition "})

# -----------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------

# END OF PROGRAM (CUSTOMER ) TRANSITION API'S

# -----------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------





# -----------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------

# API'S FOR INVOICE TRANSITION ( CUSTOMER ) 

# -----------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------

