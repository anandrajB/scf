from accounts.permission import Is_Administrator
from transaction.FSM.program import WorkFlow
from accounts.models import signatures
from transaction.FSM.upload import UploadFlow
from transaction.models import workflowitems 
from transaction.permission.program_permission import (
    Is_Accepter,
    Is_Approve,
    Is_Rejecter,
    Is_administrator,
    IsAccept_Sign_A,
    IsAccept_Sign_B,
    IsAccept_Sign_C,
    IsApprove_Sign_A,
    IsApprove_Sign_B,
    IsApprove_Sign_C, 
    IsReject_Sign_A, 
    IsReject_Sign_B, 
    IsReject_Sign_C, 
    Ismaker, 
    IsSign_A , 
    IsSign_B  , 
    Is_Sign_C
)
from rest_framework.permissions import IsAuthenticated
from transaction.permission.upload_permissions import Is_Sign_C_upload, IsSign_A_upload, IsSign_B_upload, Ismaker_upload
from transaction.serializer import Workitemserializer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response




# -----------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------

# API FOR TRANSITION'S - PROGRAM (CUSTOMER )

# -----------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------


# DELETE TRANSITION VIEW

class TransitionDeleteApiview(APIView):
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

class SubmitTransitionApiView(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated,Ismaker]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        flow = WorkFlow(obj)
        flow.submit()
        obj.save()
        return Response({"status": "success", "data": "DRAFT -> SUBMIT"})


# UPDATE SIGN_A SUBMIT TRANSITION -  anand 24 jan

class SubmitTransitionSign_AApiview(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated,IsSign_A ]
        
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

class SubmitTransitionSign_BApiview(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated,IsSign_B]

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

class SubmitTransitionSign_CApiview(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated,Is_Sign_C]

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

class RejectTransitionApiView(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated,Is_Administrator]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        flow = WorkFlow(obj)
        flow.reject()
        obj.save()
        return Response({"ok changed => REJECT"})


# REJECT SIGN_A TRANSITION

class RejectSign_AApiview(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated,IsReject_Sign_A]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user.party
        signs = signatures.objects.get(party=user, action__desc__contains='REJECT', model='PROGRAM')
        if user.party_type == "BANK":
            if signs.sign_a == True:
                flow = WorkFlow(obj)
                flow.reject_level_1()
                obj.save()
                return Response({"status": "success", "data": "SUBMIT : sign_A transition done"})
            else:
                return Response({"data": "can't do this transition"})
        else:
            return Response({"data":"can't do this transition "})
       


# REJECT SIGN_B TRANSITION


class RejectSign_BApiview(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated,IsReject_Sign_B]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user.party
        signs = signatures.objects.get(party=user, action__desc__contains='REJECT', model='PROGRAM')
        if user.party_type  == "BANK":
            if signs.sign_b == True:
                flow = WorkFlow(obj)
                flow.reject_level_2()
                obj.save()
                return Response({"status": "success", "data": "SUBMIT : sign_B transition done"})
            else:
                return Response({"data": "can't do this transition"})
        else:
            return Response({"data":"can't do this transition "})


# REJECT SIGN_C TRANSITION


class RejectSign_CApiview(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated,IsReject_Sign_C]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user.party
        signs = signatures.objects.get(party=user, action__desc__contains='REJECT', model='PROGRAM')
        if user.party_type == "BANK":
            if signs.sign_c == True:
                flow = WorkFlow(obj)
                flow.reject_level_3()
                obj.save()
                return Response({"status": "success", "data": "SUBMIT : sign_C transition done"})
            else:
                return Response({"data": "can't do this transition"})
        else:
            return Response({"data":"can't do this transition "})


# -----------------------------------------

# ACCEPT TRANSITIONS
# ----------------------------------------


# INITIAL ACCEPT TRANSIION


class AcceptTransitionApiview(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated,Is_Accepter]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        flow = WorkFlow(obj)
        flow.accept()
        obj.save()
        return Response({"status": "Success","data":"initial accept"})


# ACCEPT SIGN_A TRANSITION API VIEW

class AcceptSign_AApiView(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated,IsAccept_Sign_A]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user.party
        signs = signatures.objects.get(party=user, action__desc__contains='ACCEPT', model='PROGRAM')
        if user.party_type == "BANK":
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

class AcceptSign_BApiView(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated,IsAccept_Sign_B]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user.party
        signs = signatures.objects.get(party=user, action__desc__contains='ACCEPT', model='PROGRAM')
        if user.party_type == "BANK":
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

class AcceptSign_CApiView(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated,IsAccept_Sign_C]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user.party
        signs = signatures.objects.get(party=user, action__desc__contains='ACCEPT', model='PROGRAM')
        if user.party_type == "BANK":
            if signs.sign_c == True:
                flow = WorkFlow(obj)
                flow.accept_level_3()
                obj.save()
                return Response({"status": "success", "data": "ACCEPT : sign_C transition done"})
            else:
                return Response({"data": "can't do this transition"})
        else:
            return Response({"data":"can't do this transition "})



# -----------------------------------------

# APPROVE TRANSITIONS
# ----------------------------------------


# INITIAL ACCEPT TRANSIION


class ApproveTransitionApiview(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated,Is_Approve]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        flow = WorkFlow(obj)
        flow.approve()
        obj.save()
        return Response({"status": "Success","data":"initial accept"})


# ACCEPT SIGN_A TRANSITION API VIEW

class ApproveSign_AApiView(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated,IsApprove_Sign_A]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user.party
        signs = signatures.objects.get(party=user, action__desc__contains='ACCEPT', model='PROGRAM')
        if user.party_type == "BANK":
            if signs.sign_a == True:
                flow = WorkFlow(obj)
                flow.approve_signA()
                obj.save()
                return Response({"status": "success", "data": "ACCEPT : sign_A transition done"})
            else:
                return Response({"data": "can't do this transition"})
        else:
            return Response({"data":"can't do this transition "})

# ACCEPT SIGN_B TRANSITION API VIEW

class ApproveSign_BApiView(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated,IsApprove_Sign_B]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user.party
        signs = signatures.objects.get(party=user, action__desc__contains='ACCEPT', model='PROGRAM')
        if user.party_type == "BANK":
            if signs.sign_b == True:
                flow = WorkFlow(obj)
                flow.approve_signB()
                obj.save()
                return Response({"status": "success", "data": "ACCEPT : sign_B transition done"})
            else:
                return Response({"data": "can't do this transition"})
        else:
            return Response({"data":"can't do this transition "})

# ACCEPT SIGN_C TRANSITION API VIEW

class ApproveSign_CApiView(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated,IsApprove_Sign_C]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user.party
        signs = signatures.objects.get(party=user, action__desc__contains='ACCEPT', model='PROGRAM')
        if user.party_type == "BANK":
            if signs.sign_c == True:
                flow = WorkFlow(obj)
                flow.approve_signC()
                obj.save()
                return Response({"status": "success", "data": "ACCEPT : sign_C transition done"})
            else:
                return Response({"data": "can't do this transition"})
        else:
            return Response({"data":"can't do this transition "})





# -----------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------

# END OF PROGRAM (CUSTOMER & BANK ) TRANSITION API'S

# -----------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------





# -----------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------

# API'S FOR UPLOAD TRANSITION ( ONLY WITHIN - CUSTOMER ) 

# -----------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------

# Invoice Uploads Transition Views
class UploadSubmitTransitionApiView(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated, Ismaker_upload]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        print(obj.uploads)
        flow = UploadFlow(obj)
        flow.submit_draft()
        obj.save()
        return Response({"status": "success", "data": "DRAFT -> SUBMIT"})


# UPDATE SIGN_A SUBMIT TRANSITION -  anand 24 jan


class UploadSign_AApiview(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated, IsSign_A_upload]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user
        party = obj.program.party
        signs = signatures.objects.get(
            party=party, action__desc__contains='SUBMIT', model='UPLOAD')
        try:
            if user.party == party:
                if signs.sign_a == True:
                    flow = UploadFlow(obj)
                    flow.submit_A()
                    obj.save()
                    return Response({"status": "success", "data": "SUBMIT : sign_A transition done"})
                else:
                    return Response({"data": "can't do this transition"})
            else:
                return Response({"data": "can't do this transition "})
        except:
            return Response({"ok da "})


# UPDATE SIGN_B SUBMIT TRANSITION

class UploadSign_BApiview(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated, IsSign_B_upload]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user
        party = obj.program.party
        signs = signatures.objects.get(
            party=party, action__desc__contains='SUBMIT', model='UPLOAD')
        if user.party == party:
            if signs.sign_b == True:
                flow = UploadFlow(obj)
                flow.submit_B()
                obj.save()
                return Response({"status": "success", "data": "SUBMIT : sign_B transition done"})
            else:
                return Response({"data": "can't do this transition"})
        else:
            return Response({"data": "can't do this transition "})


# UPDATE SIGN_C SUBMIT TRANSITION

class UploadSign_CApiview(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated, Is_Sign_C_upload]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user
        party = obj.program.party
        signs = signatures.objects.get(
            party=party, action__desc__contains='SUBMIT', model='UPLOAD')
        if user.party == party:
            if signs.sign_c == True:
                flow = UploadFlow(obj)
                flow.submit_C()
                obj.save()
                return Response({"status": "success", "data": "SUBMIT : sign_C transition done"})
            else:
                return Response({"data": "can't do this transition"})
        else:
            return Response({"data": "can't do this transition "})