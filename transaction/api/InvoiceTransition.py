from accounts.permission.base_permission import Is_Bank, Is_Buyer, Is_Seller
from accounts.models import signatures , userprocessauth
from transaction.FSM.invoice_bank import InvoiceBankFlow
from rest_framework import status
from transaction.models import workflowitems 
from rest_framework.permissions import IsAuthenticated
from transaction.serializer import Workitemserializer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from transaction.FSM.Invoice import InvoiceFlow



# FINANCE REQUEST TYPE ( INVOLVES  -  bank and buyer )


# -----------------------------------
#       INVOICE SUBMIT TRANSITIONS
# -----------------------------------


# SAVE , SIGN_A,B,C

class InvoiceSubmitTransitionApiview(APIView):
    queryset = workflowitems.objects.all()
    permission_classes = [Is_Buyer | Is_Bank]

    def get(self, request, pk, *args, **kwargs):
        user = request.user
        obj = generics.get_object_or_404(workflowitems, id=pk)
        signs = signatures.objects.get(party=user.party, action__desc__contains='SUBMIT', model='INVOICE')
        auth = userprocessauth.objects.get(user = user , action__desc__contains='SUBMIT',model ='INVOICE')
        type = self.request.query_params.get('type')
        flow = InvoiceFlow(obj)
        pgr_type = obj.invoice.program_type
        if type == "save" :
            if pgr_type == "APF":
                flow.Submit_APF(request)
                obj.save()
            else:
                flow.submit__draft(request)
                obj.save()
            return Response({"status": "success", "data": "initial submit success "},status= status.HTTP_200_OK)
        if type == "sign_a" and signs.sign_a == True and auth.sign_a == True:
            if pgr_type == "APF":
                flow.Submit_APF_SignA(request)
                obj.save()
            else:
                flow.submit__SignA(request)
                obj.save()
            return Response({"status": "success", "data": "SUBMIT : sign_A transition done"},status= status.HTTP_200_OK)
        if type == "sign_b" and signs.sign_b == True and auth.sign_b == True:
            if pgr_type == "APF":
                flow.Submit_APF_SignB(request)
                obj.save()
            else:
                flow.submit__SignB(request)
                obj.save()
            return Response({"status": "success", "data": "SUBMIT : sign_B transition done"},status= status.HTTP_200_OK)
        
        if type == "sign_c" and signs.sign_c == True and auth.sign_c == True:
            if pgr_type == "APF":
                flow.Submit_APF_SignC(request)
                obj.save()
            else:
                flow.submit__SignC()
                obj.save()
            return Response({"status": "success",  "data": "SUBMIT : sign_C transition done"},status= status.HTTP_200_OK)

        return Response({"status": "failure", "data": "can't do this transition "},status= status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

   
# -----------------------------------
#       REJECT TRANSITIONS
# -----------------------------------


# MAKER , SIGN_A,B,C

# SAVE , SIGN_A,B,C

class InvoiceRejectTransitionApiView(APIView):
    queryset = workflowitems.objects.all()
    permission_classes = [Is_Buyer | Is_Bank]

    def get(self, request, pk, *args, **kwargs):
        user = request.user
        obj = generics.get_object_or_404(workflowitems, id=pk)
        signs = signatures.objects.get(party=user.party, action__desc__contains='REJECT', model='INVOICE')
        auth = userprocessauth.objects.get(user = user , action__desc__contains='REJECT',model ='INVOICE')
        type = self.request.query_params.get('type')
        if type == "save" :
            if user.party.party_type == "BANK":
                flow = InvoiceBankFlow(obj)
                flow.reject_invoice(request)
                obj.save()
                return Response({"status": "success",  "data": "REJECT : initial reject by bank"},status= status.HTTP_200_OK)
            else:
                flow = InvoiceFlow(obj)
                flow.reject_APF(request)
                obj.save()
                return Response({"status": "success", "data": "REJECT success "},status= status.HTTP_200_OK)
        if type == "sign_a" and signs.sign_a == True and auth.sign_a == True:
            if user.party.party_type == "BANK":
                flow = InvoiceBankFlow(obj)
                flow.reject_inv_signA(request)
                obj.save()
                return Response({"status": "success",  "data": "REJECT : sign_A transition done by bank"},status= status.HTTP_200_OK)
            else:
                flow = InvoiceFlow(obj)
                flow.reject_APF_SignA(request)
                obj.save()
                return Response({"status": "success", "data": "REJECT : sign_A transition done"},status= status.HTTP_200_OK)
        if type == "sign_b" and signs.sign_b == True and auth.sign_b == True:
            if user.party.party_type == "BANK":
                flow = InvoiceBankFlow(obj)
                flow.reject_inv_signB(request)
                obj.save()
                return Response({"status": "success",  "data": "REJECT : sign_C transition done by bank"},status= status.HTTP_200_OK)
            else:
                flow = InvoiceFlow(obj)
                flow.reject_APF_SignB(request)
                obj.save()
                return Response({"status": "success", "data": "REJECT : sign_B transition done"},status= status.HTTP_200_OK)
        
        if type == "sign_c" and signs.sign_c == True and auth.sign_c == True:
            if user.party.party_type == "BANK":
                flow = InvoiceBankFlow(obj)
                flow.reject_inv_signC(request)
                obj.save()
                return Response({"status": "success",  "data": "REJECT : sign_C transition done"},status= status.HTTP_200_OK)
            else:
                flow = InvoiceFlow(obj)
                flow.reject_APF_SignC(request)
                obj.save()
                return Response({"status": "success",  "data": "REJECT : sign_C transition done"},status= status.HTTP_200_OK)

        return Response({"status": "failure", "data": "can't do this transition "},status= status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


# -----------------------------------
#      INVOICE APPROVE  TRANSITIONS
# -----------------------------------


class InvoiceApproveTransitionApiView(APIView):
    queryset = workflowitems.objects.all()
    permission_classes = [Is_Buyer | Is_Bank]

    def get(self, request, pk, *args, **kwargs):
        user = request.user
        obj = generics.get_object_or_404(workflowitems, id=pk)
        signs = signatures.objects.get(party=user.party, action__desc__contains='APPROVE', model='INVOICE')
        auth = userprocessauth.objects.get(user = user , action__desc__contains='APPROVE',model ='INVOICE')
        type = self.request.query_params.get('type')
        if type == "save" :
            if user.party.party_type == "BANK":
                flow = InvoiceBankFlow(obj)
                flow.approve_invoice(request)
                obj.save()
                return Response({"status": "success", "data": "intial APPROVE BY BANK"})
            else:
                flow = InvoiceFlow(obj)
                flow.approve_APF(request)
                obj.save()
                return Response({"status": "success", "data": "intial APPROVE BY BUYER "})
        if type == "sign_a" and signs.sign_a == True and auth.sign_a == True:
            if user.party.party_type == "BANK":
                flow = InvoiceBankFlow(obj)
                flow.approve_inv_signA(request)
                obj.save()
                return Response({"status": "success", "data": "SUBMIT : sign_A transition done"},status= status.HTTP_200_OK)
            else:
                flow = InvoiceFlow(obj)
                flow.approve_APF_SignA(request)
                obj.save()
                return Response({"status": "success", "data": "SUBMIT : sign_A transition done"},status= status.HTTP_200_OK)
        if type == "sign_b" and signs.sign_b == True and auth.sign_b == True:
            if user.party.party_type == "BANK":
                flow = InvoiceBankFlow(obj)
                flow.approve_inv_signB(request)
                obj.save()
                return Response({"status": "success", "data": "SUBMIT : sign_A transition done"},status= status.HTTP_200_OK)
            else:
                flow = InvoiceFlow(obj)
                flow.approve_APF_SignB(request)
                obj.save()
                return Response({"status": "success", "data": "SUBMIT : sign_B transition done"},status= status.HTTP_200_OK)
        
        if type == "sign_c" and signs.sign_c == True and auth.sign_c == True:
            if user.party.party_type == "BANK":
                flow = InvoiceBankFlow(obj)
                flow.approve_inv_signC(request)
                obj.save()
                return Response({"status": "success", "data": "SUBMIT : sign_A transition done"},status= status.HTTP_200_OK)
            else:
                flow = InvoiceFlow(obj)
                flow.approve_APF_SignC(request)
                obj.save()
                return Response({"status": "success",  "data": "SUBMIT : sign_C transition done"},status= status.HTTP_200_OK)

        return Response({"status": "failure", "data": "can't do this transition "},status= status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


# -----------------------------------#
#   REQUEST FINANCE   TRANSITIONS    #
# -----------------------------------#


class InvoiceRequestFinanceTransitionApi(APIView):
    queryset = workflowitems.objects.all()
    permission_classes = [ IsAuthenticated,Is_Seller ]

    def get(self, request, pk, *args, **kwargs):
        user = request.user
        obj = generics.get_object_or_404(workflowitems, id=pk)
        signs = signatures.objects.get(party=user.party, action__desc__contains='REQUEST FINANCE', model='INVOICE')
        auth = userprocessauth.objects.get(user = user , action__desc__contains='REQUEST FINANCE',model ='INVOICE')
        type = self.request.query_params.get('type')
        flow = InvoiceFlow(obj)
        if type == "save" :
            if obj.action == "REJECT":
                obj.initial_state = "FINANCE_REJECTED"
                flow.REQ_FIN_APF(request)
                obj.save()
                return Response({"status": "success", "data": "intial finance request"})
            elif obj.action == "APPROVE":
                obj.initial_state = "APPROVED_BY_BUYER"
                flow.REQ_FIN_APF(request)
                obj.save()
                return Response({"status": "success", "data": "intial request finance by seller"})
        if type == "sign_a" and signs.sign_a == True and auth.sign_a == True:
            flow.REQ_FIN_APF_SignA(request)
            obj.save()
            return Response({"status": "success", "data": "REQUEST FINANCE : sign_A transition done"})
        if type == "sign_b" and signs.sign_b == True and auth.sign_b == True:
            flow.REQ_FIN_APF_SignB(request)
            obj.save()
            return Response({"status": "success", "data": "REQUEST FINANCE : sign_B transition done"})
        if type == "sign_c" and signs.sign_c == True and auth.sign_c == True:
            flow.REQ_FIN_APF_SignC(request)
            obj.save()
            return Response({"status": "success", "data": "REQUEST FINANCE : sign_C transition done"})
        return Response({"status": "failure", "data": "can't do this transition "},status= status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)



# -----------------------------------#
#    INVOICE ARCHIVE  TRANSITIONS    #
# -----------------------------------#


class InvoiceArchiveTransitionApi(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [Is_Buyer | Is_Bank]


    def get(self, request, pk, *args, **kwargs):
        user = request.user
        obj = generics.get_object_or_404(workflowitems, id=pk)
        signs = signatures.objects.get(party=user.party, action__desc__contains='ARCHIVE', model='INVOICE')
        auth = userprocessauth.objects.get(user = user , action__desc__contains='ARCHIVE',model ='INVOICE')
        type = self.request.query_params.get('type')
        flow = InvoiceFlow(obj)
        if type == "save" :
            flow.Archive_APF(request)
            obj.save()
            return Response({"status": "success", "data": "initial archive success "},status= status.HTTP_200_OK)
        if type == "sign_a" and signs.sign_a == True and auth.sign_a == True:
            flow.Archive_APF_SignA(request)
            obj.save()
            return Response({"status": "success", "data": "ARCHIVE : sign_A transition done"},status= status.HTTP_200_OK)
        if type == "sign_b" and signs.sign_b == True and auth.sign_b == True:
            flow.Archive_APF_SignB(request)
            obj.save()
            return Response({"status": "success", "data": "ARCHIVE : sign_B transition done"},status= status.HTTP_200_OK)
        
        if type == "sign_c" and signs.sign_c == True and auth.sign_c == True:
            flow.Archive_APF_SignC(request)
            obj.save()
            return Response({"status": "success",  "data": "ARCHIVE : sign_C transition done"},status= status.HTTP_200_OK)

        return Response({"status": "failure", "data": "can't do this transition "},status= status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)





# -----------------------------------#
#    INVOICE SETTLE  TRANSITIONS    #
# -----------------------------------#


class InvoiceSettleTransitionApi(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [ Is_Bank ]


    def get(self, request, pk, *args, **kwargs):
        user = request.user
        obj = generics.get_object_or_404(workflowitems, id=pk)
        signs = signatures.objects.get(party=user.party, action__desc__contains='SETTLE', model='INVOICE')
        auth = userprocessauth.objects.get(user = user , action__desc__contains='SETTLE',model ='INVOICE')
        type = self.request.query_params.get('type')
        flow = InvoiceBankFlow(obj)
        if type == "save" :
            flow.settle_invoice(request)
            obj.save()
            return Response({"status": "success", "data": "initial settle success "},status= status.HTTP_200_OK)
        if type == "sign_a" and signs.sign_a == True and auth.sign_a == True:
            flow.settle_signA(request)
            obj.save()
            return Response({"status": "success", "data": "SETTLE : sign_A transition done"},status= status.HTTP_200_OK)
        if type == "sign_b" and signs.sign_b == True and auth.sign_b == True:
            flow.settle_signB(request)
            obj.save()
            return Response({"status": "success", "data": "SETTLE : sign_B transition done"},status= status.HTTP_200_OK)
        
        if type == "sign_c" and signs.sign_c == True and auth.sign_c == True:
            flow.settle_signC(request)
            obj.save()
            return Response({"status": "success",  "data": "SETTLE : sign_C transition done"},status= status.HTTP_200_OK)

        return Response({"status": "failure", "data": "can't do this transition "},status= status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


# -----------------------------------#
#    INVOICE OVERDUE  TRANSITIONS    #
# -----------------------------------#


class InvoiceOverdueTransitionApi(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [ Is_Bank ]


    def get(self, request, pk, *args, **kwargs):
        user = request.user
        obj = generics.get_object_or_404(workflowitems, id=pk)
        signs = signatures.objects.get(party=user.party, action__desc__contains='OVERDUE', model='INVOICE')
        auth = userprocessauth.objects.get(user = user , action__desc__contains='OVERDUE',model ='INVOICE')
        type = self.request.query_params.get('type')
        flow = InvoiceBankFlow(obj)
        if type == "save" :
            flow.overdue_invoice(request)
            obj.save()
            return Response({"status": "success", "data": "initial overdue success "},status= status.HTTP_200_OK)
        if type == "sign_a" and signs.sign_a == True and auth.sign_a == True:
            flow.overdue_signA(request)
            obj.save()
            return Response({"status": "success", "data": "OVERDUE : sign_A transition done"},status= status.HTTP_200_OK)
        if type == "sign_b" and signs.sign_b == True and auth.sign_b == True:
            flow.overdue_signB(request)
            obj.save()
            return Response({"status": "success", "data": "OVERDUE : sign_B transition done"},status= status.HTTP_200_OK)
        
        if type == "sign_c" and signs.sign_c == True and auth.sign_c == True:
            flow.overdue_signC(request)
            obj.save()
            return Response({"status": "success",  "data": "OVERDUE : sign_C transition done"},status= status.HTTP_200_OK)

        return Response({"status": "failure", "data": "can't do this transition "},status= status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)





# ------------------------------------
#       OTHER  TRANSITIONS
# -----------------------------------

class InvoiceReturnTransitionApiView(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [Is_Bank | Is_Buyer]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = request.user
        if user.party.party_type == "BANK":
            flow = InvoiceBankFlow(obj)
            flow.Return_Bank_Invoice(request)
            obj.save()
        else:
            flow = InvoiceFlow(obj)
            flow.Return_Invoice(request)
            obj.save()
        return Response({"status": "Success", "data": "RETURN"},status= status.HTTP_200_OK)
