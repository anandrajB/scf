
# class InboxListApiview(APIView, PageNumberPagination):
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self, request):
#         queryset = workflowitems.objects.all()
#         user = request.user
#         record_type = request.GET.get("record_type", "")

#         if record_type == "PROGRAM":
#             queryset = workflowitems.objects.filter(
#                 current_to_party__name__contains=self.request.user.party.name, type="PROGRAM").exclude(interim_state='DRAFT').order_by('created_date')

#         elif record_type == "INVOICE":
#             queryset = workflowitems.objects.filter(Q(interim_state='AWAITING_BUYER_APPROVAL') | Q(interim_state='APPROVED_BY_BUYER') | Q(
#                 interim_state='REJECTED_BY_BUYER'), current_to_party__name__contains=user.party.name, type="INVOICE").order_by('created_date')

#         elif record_type == "FINANCE_REQUEST":
#             queryset = workflowitems.objects.filter(Q(interim_state='FINANCE_REQUESTED') | Q(interim_state='FINANCE_REJECTED') | Q(
#                 interim_state='FINANCED'), current_to_party__name__contains=user.party.name, type="INVOICE").order_by('created_date')
        
#         elif record_type == "AW_SIGN":
#             queryset = workflowitems.objects.filter(current_from_party__name__contains=request.user.party.name, next_available_transitions__isnull='')

#         return queryset.filter(current_to_party__name__contains=user.party.name).exclude(Q(interim_state='DRAFT') | Q(interim_state='COMPLETED')).order_by('created_date')

#     def get(self, request, *args, **kwargs):
#         datas = self.get_queryset(request)
#         results = self.paginate_queryset(datas, request)
#         serializer = Workitemsmessagesawapserializer(results, many=True)
#         return self.get_paginated_response(serializer.data)



# # SENT API

# class SentListApiview(ListAPIView):
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self, request):
#         queryset = workevents.objects.all()
#         user = self.request.user
#         record_type = request.GET.get("record_type", "")
#         if record_type == "PROGRAM":
#             queryset = workevents.objects.filter(from_party__name__contains=user.party.name, type='PROGRAM',
#                                                  final="YES").exclude(interim_state='DRAFT').order_by('created_date')

#         elif record_type == "INVOICE":
#             queryset = workevents.objects.filter(Q(interim_state='AWAITING_BUYER_APPROVAL') | Q(interim_state='APPROVED_BY_BUYER') | Q(
#                 interim_state='REJECTED_BY_BUYER'), from_party__name__contains=user.party.name, type='INVOICE',  final="YES").order_by('created_date')

#         elif record_type == "FINANCE_REQUEST":
#             queryset = workevents.objects.filter(Q(interim_state='FINANCE_REQUESTED') | Q(interim_state='FINANCE_REJECTED') | Q(
#                 interim_state='FINANCED'), from_party__name__contains=user.party.name, type='INVOICE',  final="YES").order_by('created_date')
        
        

#         return queryset.filter(from_party__name__contains=user.party.name, final="YES").exclude(interim_state='DRAFT').order_by('created_date')

#     def list(self, request, *args, **kwargs):
#         var = self.get_queryset(request)
#         serializer = Workeventsmessageserializer(var, many=True)
#         return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


# # SENT AWAITING SIGN API

# class SentAwaitingSignApiview(ListAPIView):
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self, request):
#         queryset = workflowitems.objects.all()
#         user = self.request.user
#         record_type = request.GET.get("record_type", "")
#         if record_type == "PROGRAM":
#             queryset = workflowitems.objects.filter(current_from_party__name__contains=user.party.name, type='PROGRAM',
#                                                     next_available_transitions__isnull='').exclude(interim_state='DRAFT').order_by('created_date')

#         elif record_type == "INVOICE":
#             queryset = workflowitems.objects.filter(Q(interim_state='AWAITING_BUYER_APPROVAL') | Q(interim_state='APPROVED_BY_BUYER') | Q(
#                 interim_state='REJECTED_BY_BUYER'), current_from_party__name__contains=user.party.name, type='INVOICE', next_available_transitions__isnull='').order_by('created_date')

#         elif record_type == "FINANCE_REQUEST":
#             queryset = workflowitems.objects.filter(Q(interim_state='FINANCE_REQUESTED') | Q(interim_state='FINANCE_REJECTED') | Q(
#                 interim_state='FINANCED'), current_from_party__name__contains=user.party.name, type='INVOICE', next_available_transitions__isnull='').order_by('created_date')

#         return queryset.filter(current_from_party__name__contains=user.party.name, next_available_transitions__isnull='').exclude(interim_state='DRAFT').order_by('created_date')

#     def list(self, request, *args, **kwargs):
#         var = self.get_queryset(request)
#         serializer = Workitemsmessagesawapserializer(var, many=True)
#         return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


# # DRAFT API VIEW

# class DraftListApiview(ListAPIView):
#     permission_classes = [IsAuthenticated]


#     def list(self, request, *args, **kwargs):
#         var = workflowitems.objects.filter(current_from_party__name__contains=self.request.user.party.name,
#                                            initial_state='DRAFT', interim_state='DRAFT').order_by('created_date')
#         serializer = Workitemsmessagesawapserializer(var, many=True)
#         return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


# # AWAITING APPROVAL API

# class AwaitingApprovalMessageApiView(APIView):
#     queryset = workflowitems.objects.all()
#     serializer_class = Workitemsmessagesawapserializer
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         var = workflowitems.objects.filter(
#             current_from_party__name__contains=request.user.party.name, next_available_transitions__isnull='')
#         serializer = Workitemsmessagesawapserializer(var, many=True)
#         return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
