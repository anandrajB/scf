from accounts.models import signatures , userprocessauth
from transaction.FSM.upload import UploadFlow
from rest_framework import status
from transaction.models import workflowitems 
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from accounts.permission.base_permission import  Is_Seller




# --------------------------------------------------#
#    INVOICE UPLOAD  TRANSITIONS   manaual and csv  #
# --------------------------------------------------#


class InvoiceUploadTransitionApiView(APIView):
    queryset = workflowitems.objects.all() 
    permission_classes = [IsAuthenticated , Is_Seller]

    def get(self, request, pk, *args, **kwargs):
        user = request.user
        obj = generics.get_object_or_404(workflowitems, id=pk)
        signs = signatures.objects.get(party=user.party, action__desc__contains='SUBMIT', model='UPLOAD')
        auth = userprocessauth.objects.get(user = user , action__desc__contains='SUBMIT',model ='UPLOAD')
        type = self.request.query_params.get('type')
        flow = UploadFlow(obj)
        if type == "save":
            flow.submit_draft(request)
            obj.save()
            return Response({"status": "success", "data": "initial submit success "},status= status.HTTP_200_OK)
        if type == "sign_a" and signs.sign_a == True and auth.sign_a == True:
            flow.submit_A(request)
            obj.save()
            return Response({"status": "success", "data": "SUBMIT : sign_A transition done"},status= status.HTTP_200_OK)
        if type == "sign_b" and signs.sign_b == True and auth.sign_b == True:
            flow.submit_B(request)
            obj.save()
            return Response({"status": "success", "data": "SUBMIT : sign_B transition done"},status= status.HTTP_200_OK)
        
        if type == "sign_c" and signs.sign_c == True and auth.sign_c == True:
            flow.submit_C(request)
            obj.save()
            return Response({"status": "success",  "data": "SUBMIT : sign_C transition done"},status= status.HTTP_200_OK)

        return Response({"status": "failure", "data": "can't do this transition "},status= status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


# ----------------------------#
#    INVOICE UPLOAD  RETURN   #
# ----------------------------#


class InvoiceUploadReturnTransitionview(APIView):
    queryset = workflowitems.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        flow = UploadFlow(obj)
        flow.invoice_upload_returns(request)
        obj.save()
        return Response({"status": "Success", "data": "invoice RETURN success"},status= status.HTTP_200_OK)

## help_text

# once the transition is completed , the lifecycle of individual components of invoice creation will be done .