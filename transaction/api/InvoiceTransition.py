from accounts.permission.base_permission import (
    Is_Bank,
    Is_BankAdministrator,
    Is_PartyAdministrator,
    Is_Buyer,
    Is_Seller
)
from transaction.FSM.Invoice import InvoiceFlow
from transaction.FSM.invoice_bank import InvoiceBankFlow
from accounts.models import signatures
from transaction.models import workflowitems
from transaction.serializer import Workitemserializer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


# SUBMIT TRANSITION API VIEWS

class InvoiceSubmitTransitionView(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated, Is_Seller]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        flow = InvoiceFlow(obj)
        type = obj.invoice.program_type
        if type == "APF":
            flow.Submit_APF(request)
            obj.save()
        else:
            flow.submit__draft(request)
            obj.save()
        return Response({"status": "success", "data": " SUBMIT"})


# SUBMIT SIGN_A

class InvoiceSubmitSign_ATransitionApi(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated, Is_Seller]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        flow = InvoiceFlow(obj)
        user = request.user
        type = obj.invoice.program_type
        signs = signatures.objects.get(
            party=user.party, action__desc__contains='SUBMIT', model='INVOICE')
        if signs.sign_a == True:
            if type == "APF":
                flow.Submit_APF_SignA(request)
                obj.save()
                return Response({"status": "success", "data": "SUBMIT APF : sign_A transition done"})
            else:
                flow.submit__SignA(request)
                obj.save()
                return Response({"status": "success", "data": "SUBMIT RF/DF : sign_A transition done"})
        else:
            return Response({"data": "can't do this transition"})


# SUBMIT SIGN_B

class InvoiceSubmitSign_BTransitionApi(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated, Is_Seller, Is_PartyAdministrator]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = request.user
        type = obj.invoice.program_type
        flow = InvoiceFlow(obj)
        signs = signatures.objects.get(
            party=user.party, action__desc__contains='SUBMIT', model='INVOICE')
        if signs.sign_b == True:
            if type == "APF":
                flow.Submit_APF_SignB(request)
                obj.save()
                return Response({"status": "success", "data": "SUBMIT APF : sign_B transition done"})
            else:
                flow.submit__SignB(request)
                obj.save()
                return Response({"status": "success", "data": "SUBMIT RF/DF : sign_B transition done"})
        else:
            return Response({"data": "can't do this transition"})


# SUBMIT SIGN_C

class InvoiceSubmitSign_CTransitionApi(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated, Is_Seller, Is_PartyAdministrator]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = request.user
        flow = InvoiceFlow(obj)
        type = obj.invoice.program_type
        signs = signatures.objects.get(
            party=user.party, action__desc__contains='SUBMIT', model='INVOICE')
        if signs.sign_c == True:
            if type == "APF":
                flow.Submit_APF_SignC(request)
                obj.save()
                return Response({"status": "success", "data": "SUBMIT APF : sign_C transition done"})
            else:
                flow.submit__SignC()
                obj.save()
                return Response({"status": "success", "data": "SUBMIT RF/DF : sign_C transition done"})
        else:
            return Response({"data": "can't do this transition"})


# APPROVE TRANSITION VIEWSETS

class InvoiceApproveTransitionApiView(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        user = self.request.user
        obj = generics.get_object_or_404(workflowitems, id=pk)

        if user.party.party_type == "BANK":
            flow = InvoiceBankFlow(obj)
            flow.approve_invoice(request)
            return Response({"status": "success", "data": "intial APPROVE"})
        else:
            flow = InvoiceFlow(obj)
            flow.approve_APF(request)
            obj.save()
            return Response({"status": "success", "data": "intial APPROVE"})


class InvoiceApproveSign_ATransitionApiView(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user
        party = request.user.party
        signs = signatures.objects.get(
            party=party, action__desc__contains='APPROVE', model='INVOICE')

        if user.party.party_type == "BANK":
            if signs.sign_a == True:
                flow = InvoiceBankFlow(obj)
                flow.approve_inv_signA(request)
                obj.save()
                return Response({"status": "success", "data": "APPROVE : sign_A transition done"})
            else:
                return Response({"data": "can't do this transition"})
        elif(user.party.party_type == "BUYER"):
            if signs.sign_a == True:
                flow = InvoiceFlow(obj)
                flow.approve_APF_SignA(request)
                obj.save()

                return Response({"status": "success", "data": "APPROVE : sign_A transition done"})
            else:
                return Response({"data": "can't do this transition"})


class InvoiceApproveSign_BTransitionApiView(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user
        party = request.user.party
        signs = signatures.objects.get(
            party=party, action__desc__contains='APPROVE', model='INVOICE')

        if user.party.party_type == "BANK":
            if signs.sign_b == True:
                flow = InvoiceBankFlow(obj)
                flow.approve_inv_signB(request)
                obj.save()
                return Response({"status": "success", "data": "APPROVE : sign_B transition done"})
            else:
                return Response({"data": "can't do this transition"})

        elif(user.party.party_type == "BUYER"):
            if signs.sign_b == True:
                flow = InvoiceFlow(obj)
                flow.approve_APF_SignB(request)
                obj.save()
                return Response({"status": "success", "data": "APPROVE : sign_B transition done"})
            else:
                return Response({"data": "can't do this transition"})


class InvoiceApproveSign_CTransitionApiView(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user
        party = request.user.party
        signs = signatures.objects.get(
            party=party, action__desc__contains='APPROVE', model='INVOICE')

        if user.party.party_type == "BANK":
            if signs.sign_c == True:
                flow = InvoiceBankFlow(obj)
                flow.approve_inv_signC(request)
                obj.save()
                return Response({"status": "success", "data": "APPROVE : sign_C transition done"})
            else:
                return Response({"data": "can't do this transition"})
        elif(user.party.party_type == "BUYER"):
            if signs.sign_c == True:
                flow = InvoiceFlow(obj)
                flow.approve_APF_SignC(request)
                obj.save()
                return Response({"status": "success", "data": "APPROVE : sign_C transition done"})
            else:
                return Response({"data": "can't do this transition"})


# REJECT TRANSITION VIEWSETS

class InvoiceRejectTransitionApiView(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        user = self.request.user
        obj = generics.get_object_or_404(workflowitems, id=pk)
        if user.party.party_type == "BANK":
            flow = InvoiceBankFlow(obj)
            flow.reject_invoice(request)
            return Response({"status": "success", "data": "intial reject by BANK"})
        else:
            flow = InvoiceFlow(obj)
            flow.reject_APF(request)
            obj.save()
            return Response({"status": "success", "data": "Initial reject"})


class InvoiceRejectSign_ATransitionApiView(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user
        signs = signatures.objects.get(
            party=user.party, action__desc__contains='REJECT', model='INVOICE')
        if user.party.party_type == "BANK":

            if signs.sign_a == True:
                flow = InvoiceBankFlow(obj)
                flow.reject_inv_signA(request)
                obj.save()
                return Response({"status": "success", "data": "REJECT : sign_A transition done"})
            else:
                return Response({"data": "can't do this transition"})
        elif(user.party.party_type == "BUYER"):
            if signs.sign_a == True:
                flow = InvoiceFlow(obj)
                flow.reject_APF_SignA(request)
                obj.save()
                return Response({"status": "success", "data": "REJECT : sign_A transition done"})
            else:
                return Response({"data": "can't do this transition"})


class InvoiceRejectSign_BTransitionApiView(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated, Is_Bank, Is_BankAdministrator |
                          IsAuthenticated, Is_Buyer, Is_PartyAdministrator]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user.party
        signs = signatures.objects.get(
            party=user, action__desc__contains='REJECT', model='INVOICE')

        if user.party.party_type == "BANK":

            if signs.sign_b == True:
                flow = InvoiceBankFlow(obj)
                flow.reject_inv_signB(request)
                obj.save()
                return Response({"status": "success", "data": "REJECT : sign_A transition done"})
            else:
                return Response({"data": "can't do this transition"})
        elif(user.party.party_type == "BUYER"):
            if signs.sign_b == True:
                flow = InvoiceFlow(obj)
                flow.reject_APF_SignB(request)
                obj.save()
                return Response({"status": "success", "data": "REJECT : sign_A transition done"})
            else:
                return Response({"data": "can't do this transition"})


class InvoiceRejectSign_CTransitionApiView(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated, Is_Bank, Is_BankAdministrator |
                          IsAuthenticated, Is_Buyer, Is_PartyAdministrator]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user.party
        signs = signatures.objects.get(
            party=user, action__desc__contains='REJECT', model='INVOICE')

        if user.party.party_type == "BANK":

            if signs.sign_c == True:
                flow = InvoiceBankFlow(obj)
                flow.reject_inv_signC(request)
                obj.save()
                return Response({"status": "success", "data": "REJECT : sign_A transition done"})
            else:
                return Response({"data": "can't do this transition"})
        elif(user.party.party_type == "BUYER"):
            if signs.sign_c == True:
                flow = InvoiceFlow(obj)
                flow.reject_APF_SignC(request)
                obj.save()
                return Response({"status": "success", "data": "REJECT : sign_A transition done"})
            else:
                return Response({"data": "can't do this transition"})


# ---------------------------------------REQUEST FINANCE--------------------------------------


class REQ_FIN_TransitionAPIView(APIView):

    queryset = workflowitems.objects.all()

    serializer_class = Workitemserializer

    permission_classes = [IsAuthenticated, Is_Seller]

    def get(self, request, pk, *args, **kwargs):

        obj = generics.get_object_or_404(workflowitems, id=pk)

        flow = InvoiceFlow(obj)

        if obj.action == "REJECT":
            obj.initial_state = "FINANCE_REJECTED"
            flow.REQ_FIN_APF(request)

            obj.save()

        elif obj.action == "APPROVE":
            obj.initial_state = "APPROVED BY BUYER"
            flow.REQ_FIN_APF(request)
            obj.save()

        return Response({"status": "Success", "data": "initial Request Finance"})


class REQ_FIN_SignA_APF(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated, Is_Seller]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user.party
        signs = signatures.objects.get(
            party=user, action__desc__contains='REQUEST FINANCE', model='INVOICE')
        if signs.sign_a == True:
            flow = InvoiceFlow(obj)
            flow.REQ_FIN_APF_SignA(request)
            obj.save()
            return Response({"status": "success", "data": "REQUEST FINANCE : sign_A transition done"})

        else:
            return Response({"data": "can't do this transition "})


class REQ_FIN_SignB_APF(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated, Is_Seller]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user.party
        signs = signatures.objects.get(
            party=user, action__desc__contains='REQUEST FINANCE', model='INVOICE')

        if signs.sign_b == True:
            flow = InvoiceFlow(obj)
            flow.REQ_FIN_APF_SignB(request)
            obj.save()
            return Response({"status": "success", "data": "REQUEST FINANCE : sign_B transition done"})

        else:
            return Response({"data": "can't do this transition "})


class REQ_FIN_SignC_APF(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated, Is_Seller, Is_PartyAdministrator]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user.party
        signs = signatures.objects.get(
            party=user, action__desc__contains='REQUEST FINANCE', model='INVOICE')
        if signs.sign_c == True:
            flow = InvoiceFlow(obj)
            flow.REQ_FIN_APF_SignC(request)
            obj.save()
            return Response({"status": "success", "data": "REQUEST FINANCE : sign_C transition done"})
        else:
            return Response({"data": "can't do this transition "})


# -----------------------------------ARCHIVE-----------------------------------


class Archive_APIView_APF(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        flow = InvoiceFlow(obj)
        flow.Archive_APF()
        obj.save()
        return Response({"status": "success", "data": "REJECTED BY BUYER -> ARCHIVED"})


class ArchiveTransition_APF_SignA(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user
        party = obj.program.party
        signs = signatures.objects.get(
            party=party, action__desc__contains='ARCHIVE', model='INVOICE')
        if user.party == party:
            if signs.sign_a == True:
                flow = InvoiceFlow(obj)
                flow.Archive_APF_SignA()
                obj.save()
                return Response({"status": "success", "data": "ARCHIVE : sign_A transition done"})
            else:
                return Response({"data": "can't do this transition"})
        else:
            return Response({"data": "can't do this transition "})


class ArchiveTransition_APF_SignB(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user
        party = obj.program.party
        signs = signatures.objects.get(
            party=party, action__desc__contains='ARCHIVE', model='INVOICE')
        if user.party == party:
            if signs.sign_a == True:
                flow = InvoiceFlow(obj)
                flow.Archive_APF_SignB()
                obj.save()
                return Response({"status": "success", "data": "ARCHIVE : sign_B transition done"})
            else:
                return Response({"data": "can't do this transition"})
        else:
            return Response({"data": "can't do this transition "})


class ArchiveTransition_APF_SignC(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user
        party = obj.program.party
        signs = signatures.objects.get(
            party=party, action__desc__contains='ARCHIVE', model='INVOICE')
        if user.party == party:
            if signs.sign_a == True:
                flow = InvoiceFlow(obj)
                flow.Archive_APF_SignC()
                obj.save()
                return Response({"status": "success", "data": "ARCHIVE : sign_C transition done"})
            else:
                return Response({"data": "can't do this transition"})
        else:
            return Response({"data": "can't do this transition "})


# # -----SUBMIT TRANSITION API FOR RF AND DF TYPE--------------------------------------


# class SubmitTransitionSign_AApiview_RFDF(APIView):
#     queryset = workflowitems.objects.all()
#     serializer_class = Workitemserializer
#     permission_classes = [IsAuthenticated]

#     def get(self, request, pk, *args, **kwargs):
#         obj = generics.get_object_or_404(workflowitems, id=pk)
#         user = self.request.user
#         party = obj.program.party
#         signs = signatures.objects.get(
#             party=party, action__desc__contains='SUBMIT', model='INVOICE')
#         if user.party == party:
#             if signs.sign_a == True:
#                 flow = InvoiceFlow(obj)
#                 flow.submit__SignA()
#                 obj.save()
#                 return Response({"status": "success", "data": "SUBMIT : sign_A transition done"})
#             else:
#                 return Response({"data": "can't do this transition"})
#         else:
#             return Response({"data": "can't do this transition "})


# class SubmitTransitionSign_BApiview_RFDF(APIView):
#     queryset = workflowitems.objects.all()
#     serializer_class = Workitemserializer
#     permission_classes = [IsAuthenticated]

#     def get(self, request, pk, *args, **kwargs):
#         obj = generics.get_object_or_404(workflowitems, id=pk)
#         user = self.request.user
#         party = obj.program.party
#         signs = signatures.objects.get(
#             party=party, action__desc__contains='SUBMIT', model='INVOICE')
#         if user.party == party:
#             if signs.sign_a == True:
#                 flow = InvoiceFlow(obj)
#                 flow.submit__SignB()
#                 obj.save()
#                 return Response({"status": "success", "data": "SUBMIT : sign_B transition done"})
#             else:
#                 return Response({"data": "can't do this transition"})
#         else:
#             return Response({"data": "can't do this transition "})


# class SubmitTransitionSign_CApiview_RFDF(APIView):
#     queryset = workflowitems.objects.all()
#     serializer_class = Workitemserializer
#     permission_classes = [IsAuthenticated]

#     def get(self, request, pk, *args, **kwargs):
#         obj = generics.get_object_or_404(workflowitems, id=pk)
#         user = self.request.user
#         party = obj.program.party
#         signs = signatures.objects.get(
#             party=party, action__desc__contains='SUBMIT', model='INVOICE')
#         if user.party == party:
#             if signs.sign_a == True:
#                 flow = InvoiceFlow(obj)
#                 flow.submit__SignC()
#                 obj.save()
#                 return Response({"status": "success", "data": "SUBMIT : sign_C transition done"})
#             else:
#                 return Response({"data": "can't do this transition"})
#         else:
#             return Response({"data": "can't do this transition "})
