from accounts.permission import Is_Administrator
from transaction.FSM.Invoice import InvoiceFlow
from accounts.models import signatures
from transaction.models import workflowitems
from transaction.serializer import Workitemserializer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


# SUBMIT TRANSITION API VIEWS


class SubmitTransitionApiView_APF(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        flow = InvoiceFlow(obj)
        type = obj.invoice.program_type
        if type == "APF":
            flow.Submit_APF()
            obj.save()
        else:
            flow.submit__draft()
            obj.save()
        return Response({"status": "success", "data": " SUBMIT"})


class SubmitTransitionSign_AApiview_APF(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user
        party = obj.invoice.party
        type = obj.invoice.program_type
        signs = signatures.objects.get(party=party, action__desc__contains='SUBMIT', model='INVOICE')
        if signs.sign_a == True and user.party == party :
            if type == "APF":
                flow = InvoiceFlow(obj)
                flow.Submit_APF_SignA()
                obj.save()
                return Response({"status": "success", "data": "SUBMIT : sign_A transition done"})
            else:
                flow = InvoiceFlow(obj)
                flow.submit__SignA()
                obj.save()
                return Response({"status": "success", "data": "SUBMIT : sign_A transition done"})
        else:
            return Response({"data": "can't do this transition"})
        


class SubmitTransitionSign_BApiview_APF(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user
        party = obj.invoice.party
        type = obj.invoice.program_type
        signs = signatures.objects.get(party=party, action__desc__contains='SUBMIT', model='INVOICE')
        if signs.sign_b == True and user.party == party :
            if type == "APF":
                flow = InvoiceFlow(obj)
                flow.Submit_APF_SignB()
                obj.save()
                return Response({"status": "success", "data": "SUBMIT : sign_B transition done"})
            else:
                flow = InvoiceFlow(obj)
                flow.submit__SignB()
                obj.save()
                return Response({"status": "success", "data": "SUBMIT : sign_B transition done"})
        else:
            return Response({"data": "can't do this transition"})


class SubmitTransitionSign_CApiview_APF(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user
        party = obj.invoice.party
        type = obj.invoice.program_type
        signs = signatures.objects.get(party=party, action__desc__contains='SUBMIT', model='INVOICE')
        if signs.sign_c == True and user.party == party :
            if type == "APF":
                flow = InvoiceFlow(obj)
                flow.Submit_APF_SignC()
                obj.save()
                return Response({"status": "success", "data": "SUBMIT : sign_C transition done"})
            else:
                flow = InvoiceFlow(obj)
                flow.submit__SignC()
                obj.save()
                return Response({"status": "success", "data": "SUBMIT : sign_C transition done"})
        else:
            return Response({"data": "can't do this transition"})


# APPROVE TRANSITION VIEWSETS

class ApproveTransitionApiView(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        flow = InvoiceFlow(obj)
        flow.approve_APF()
        obj.save()
        return Response({"status": "success", "data": "DRAFT -> APPROVE"})


class ApproveTransiton_SignA_APF(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user
        party = obj.program.party
        signs = signatures.objects.get(party=party, action__desc__contains='APPROVE', model='INVOICE')
        if user.party == party:
            if signs.sign_a == True:
                flow = InvoiceFlow(obj)
                flow.approve_APF_SignA()
                obj.save()
                return Response({"status": "success", "data": "APPROVE : sign_A transition done"})
            else:
                return Response({"data": "can't do this transition"})
        else:
            return Response({"data": "can't do this transition "})


class ApproveTransiton_SignB_APF(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user
        party = obj.program.party
        signs = signatures.objects.get(
            party=party, action__desc__contains='APPROVE', model='INVOICE')
        if user.party == party:
            if signs.sign_a == True:
                flow = InvoiceFlow(obj)
                flow.approve_APF_SignB()
                obj.save()
                return Response({"status": "success", "data": "APPROVE : sign_B transition done"})
            else:
                return Response({"data": "can't do this transition"})
        else:
            return Response({"data": "can't do this transition "})


class ApproveTransiton_SignC_APF(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user
        party = obj.program.party
        signs = signatures.objects.get(
            party=party, action__desc__contains='APPROVE', model='INVOICE')
        if user.party == party:
            if signs.sign_a == True:
                flow = InvoiceFlow(obj)
                flow.approve_APF_SignC()
                obj.save()
                return Response({"status": "success", "data": "APPROVE : sign_Cs transition done"})
            else:
                return Response({"data": "can't do this transition"})
        else:
            return Response({"data": "can't do this transition "})



# REJECT TRANSITION VIEWSETS


class RejectTransitionApiView_APF(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated, Is_Administrator]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        flow = InvoiceFlow(obj)
        flow.reject_APF()
        obj.save()
        return Response({"ok changed => REJECT"})


class RejectSign_AApiview_APF(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user.party
        signs = signatures.objects.get(
            party=user, action__desc__contains='REJECT', model='INVOICE')
        if user.party_type == "BANK":
            if signs.sign_a == True:
                flow = InvoiceFlow(obj)
                flow.reject_APF_SignA()
                obj.save()
                return Response({"status": "success", "data": "REJECT : sign_A transition done"})
            else:
                return Response({"data": "can't do this transition"})
        else:
            return Response({"data": "can't do this transition "})


class RejectSign_BApiview_APF(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user.party
        signs = signatures.objects.get(
            party=user, action__desc__contains='REJECT', model='INVOICE')
        if user.party_type == "BANK":
            if signs.sign_a == True:
                flow = InvoiceFlow(obj)
                flow.reject_APF_SignB()
                obj.save()
                return Response({"status": "success", "data": "REJECT : sign_B transition done"})
            else:
                return Response({"data": "can't do this transition"})
        else:
            return Response({"data": "can't do this transition "})


class RejectSign_CApiview_APF(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user.party
        signs = signatures.objects.get(
            party=user, action__desc__contains='REJECT', model='INVOICE')
        if user.party_type == "BANK":
            if signs.sign_a == True:
                flow = InvoiceFlow(obj)
                flow.reject_APF_SignC()
                obj.save()
                return Response({"status": "success", "data": "REJECT : sign_C transition done"})
            else:
                return Response({"data": "can't do this transition"})
        else:
            return Response({"data": "can't do this transition "})


# ---------------------------------------REQUEST FINANCE--------------------------------------


class REQ_FIN_TransitionAPIView(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        flow = InvoiceFlow(obj)
        flow.REQ_FIN_APF()
        obj.save()
        return Response({"status": "Success", "data": "initial Request Finance"})


class REQ_FIN_SignA_APF(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user.party
        signs = signatures.objects.get(
            party=user, action__desc__contains='REQUEST FINANCE', model='INVOICE')
        if user.party_type == "BANK":
            if signs.sign_a == True:
                flow = InvoiceFlow(obj)
                flow.REQ_FIN_APF_SignA()
                obj.save()
                return Response({"status": "success", "data": "REQUEST FINANCE : sign_A transition done"})
            else:
                return Response({"data": "can't do this transition"})
        else:
            return Response({"data": "can't do this transition "})


class REQ_FIN_SignB_APF(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user.party
        signs = signatures.objects.get(
            party=user, action__desc__contains='REQUEST FINANCE', model='INVOICE')
        if user.party_type == "BANK":
            if signs.sign_a == True:
                flow = InvoiceFlow(obj)
                flow.REQ_FIN_APF_SignB()
                obj.save()
                return Response({"status": "success", "data": "REQUEST FINANCE : sign_B transition done"})
            else:
                return Response({"data": "can't do this transition"})
        else:
            return Response({"data": "can't do this transition "})


class REQ_FIN_SignC_APF(APIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        obj = generics.get_object_or_404(workflowitems, id=pk)
        user = self.request.user.party
        signs = signatures.objects.get(
            party=user, action__desc__contains='REQUEST FINANCE', model='INVOICE')
        if user.party_type == "BANK":
            if signs.sign_a == True:
                flow = InvoiceFlow(obj)
                flow.REQ_FIN_APF_SignC()
                obj.save()
                return Response({"status": "success", "data": "REQUEST FINANCE : sign_C transition done"})
            else:
                return Response({"data": "can't do this transition"})
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
