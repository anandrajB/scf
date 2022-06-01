from accounts.permission.base_permission import Is_Bank, Is_Buyer
from accounts.permission.program_permission import Is_Accepter, Is_Approve, Is_Rejecter, Ismaker
from transaction.FSM.program import WorkFlow
from accounts.models import signatures , userprocessauth
from rest_framework import status
from transaction.models import workflowitems 
from rest_framework.permissions import IsAuthenticated
from transaction.serializer import Workitemserializer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response




### PROGRAM


# -----------------------------------#
#       SUBMIT TRANSITIONS           #
# -----------------------------------#


# SAVE , SIGN_A,B,C

class ProgramSubmitTransitionApiview(APIView):
    queryset = workflowitems.objects.all()
    permission_classes = [ Is_Buyer |  Is_Bank]

    def get(self, request, pk, *args, **kwargs):
        user = request.user
        obj = generics.get_object_or_404(workflowitems, id=pk)
        signs = signatures.objects.get(party=user.party, action__desc__contains='SUBMIT', model='PROGRAM')
        auth = userprocessauth.objects.get(user = user , action__desc__contains='SUBMIT',model ='PROGRAM')
        type = self.request.query_params.get('type')
        flow = WorkFlow(obj)
        if type == "save" :
            flow.submit(request)
            obj.save()
            return Response({"status": "success", "data": "initial submit success "},status= status.HTTP_200_OK)
        if type == "sign_a" and signs.sign_a == True and auth.sign_a == True:
            flow.submit_level_1(request)
            obj.save()
            return Response({"status": "success", "data": "SUBMIT : sign_A transition done"},status= status.HTTP_200_OK)
        if type == "sign_b" and signs.sign_b == True and auth.sign_b == True:
            flow.submit_level_2(request)
            obj.save()
            return Response({"status": "success", "data": "SUBMIT : sign_B transition done"},status= status.HTTP_200_OK)
        
        if type == "sign_c" and signs.sign_c == True and auth.sign_c == True:
            flow.submit_level_3(request)
            obj.save()
            return Response({"status": "success",  "data": "SUBMIT : sign_C transition done"},status= status.HTTP_200_OK)

        return Response({"status": "failure", "data": "can't do this transition                 "},status= status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

   
# -----------------------------------#
#       REJECT TRANSITIONS           #
# -----------------------------------#


# MAKER , SIGN_A,B,C

class ProgramRejectTransitionApiview(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [ Is_Buyer | Is_Bank]


    def get(self, request, pk, *args, **kwargs):
        user = request.user
        obj = generics.get_object_or_404(workflowitems, id=pk)
        signs = signatures.objects.get(party=user.party, action__desc__contains='REJECT', model='PROGRAM')
        auth = userprocessauth.objects.get(user = user , action__desc__contains='REJECT',model ='PROGRAM')
        type = self.request.query_params.get('type')
        flow = WorkFlow(obj)
        if type == "save" :
            flow.reject(request)
            obj.save()
            return Response({"status": "success", "data": "initial reject success "},status= status.HTTP_200_OK)
        if type == "sign_a" and signs.sign_a == True and auth.sign_a == True:
            flow.reject_level_1(request)
            obj.save()
            return Response({"status": "success", "data": "REJECT : sign_A transition done"},status= status.HTTP_200_OK)
        if type == "sign_b" and signs.sign_b == True and auth.sign_b == True:
            flow.reject_level_2(request)
            obj.save()
            return Response({"status": "success", "data": "REJECT : sign_B transition done"},status= status.HTTP_200_OK)
        
        if type == "sign_c" and signs.sign_c == True and auth.sign_c == True:
            flow.reject_level_3(request)
            obj.save()
            return Response({"status": "success",  "data": "REJECT : sign_C transition done"},status= status.HTTP_200_OK)

        return Response({"status": "failure", "data": "can't do this transition "},status= status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)



# -----------------------------------#
#       APPROVE  TRANSITIONS         #
# -----------------------------------#


# MAKER , SIGN_A,B,C

class ProgramApproveTransitionApiview(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [  Is_Buyer | Is_Bank]


    def get(self, request, pk, *args, **kwargs):
        user = request.user
        obj = generics.get_object_or_404(workflowitems, id=pk)
        signs = signatures.objects.get(party=user.party, action__desc__contains='APPROVE', model='PROGRAM')
        auth = userprocessauth.objects.get(user = user , action__desc__contains='APPROVE',model ='PROGRAM')
        type = self.request.query_params.get('type')
        flow = WorkFlow(obj)
        if type == "save" :
            flow.approve(request)
            obj.save()
            return Response({"status": "success", "data": "initial approve success "},status= status.HTTP_200_OK)
        if type == "sign_a" and signs.sign_a == True and auth.sign_a == True:
            flow.approve_signA(request)
            obj.save()
            return Response({"status": "success", "data": "APPROVE : sign_A transition done"},status= status.HTTP_200_OK)
        if type == "sign_b" and signs.sign_b == True and auth.sign_b == True:
            flow.approve_signB(request)
            obj.save()
            return Response({"status": "success", "data": "APPROVE : sign_B transition done"},status= status.HTTP_200_OK)
        
        if type == "sign_c" and signs.sign_c == True and auth.sign_c == True:
            flow.approve_signC(request)
            obj.save()
            return Response({"status": "success",  "data": "APPROVE : sign_C transition done"},status= status.HTTP_200_OK)

        return Response({"status": "failure", "data": "can't do this transition "},status= status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


# -----------------------------------#
#       ACCEPT  TRANSITIONS          #
# -----------------------------------#

# MAKER , SIGN_A,B,C


class ProgramAcceptTransitionApiview(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [Is_Buyer | Is_Bank]


    def get(self, request, pk, *args, **kwargs):
        user = request.user
        obj = generics.get_object_or_404(workflowitems, id=pk)
        signs = signatures.objects.get(party=user.party, action__desc__contains='ACCEPT', model='PROGRAM')
        auth = userprocessauth.objects.get(user = user , action__desc__contains='ACCEPT',model ='PROGRAM')
        type = self.request.query_params.get('type')
        flow = WorkFlow(obj)
        if type == "save" :
            flow.accept(request)
            obj.save()
            return Response({"status": "success", "data": "initial accept success "},status= status.HTTP_200_OK)
        if type == "sign_a" and signs.sign_a == True and auth.sign_a == True:
            flow.accept_level_1(request)
            obj.save()
            return Response({"status": "success", "data": "ACCEPT : sign_A transition done"},status= status.HTTP_200_OK)
        if type == "sign_b" and signs.sign_b == True and auth.sign_b == True:
            flow.accept_level_2(request)
            obj.save()
            return Response({"status": "success", "data": "ACCEPT : sign_B transition done"},status= status.HTTP_200_OK)
        
        if type == "sign_c" and signs.sign_c == True and auth.sign_c == True:
            flow.accept_level_3(request)
            obj.save()
            return Response({"status": "success",  "data": "ACCEPT : sign_C transition done"},status= status.HTTP_200_OK)

        return Response({"status": "failure", "data": "can't do this transition "},status= status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


# -----------------------------------#
#       OTHER  TRANSITIONS           #
# -----------------------------------#

class ProgramReturnTransitionview(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        flow = WorkFlow(obj)
        flow.returns(request)
        obj.save()
        return Response({"status": "Success", "data": "RETURN"},status= status.HTTP_200_OK)
        

class ProgramTransitionDeleteApiview(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        flow = WorkFlow(obj)
        flow.delete(request)
        obj.save()
        return Response({"status": "Success", "data": "PROGRAM DELETED"},status= status.HTTP_200_OK)