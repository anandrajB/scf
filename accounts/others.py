
# class SignatureUpdateApiview(RetrieveUpdateAPIView):
#     queryset = signatures.objects.all()
#     serializer_class = signaturesserializer
    

#     def update(self, request, pk=None):
#         queryset = signatures.objects.all()
#         useraa = get_object_or_404(queryset, pk=pk)
#         print(useraa.workflowitem.id)
#         serializer = signaturesserializer(useraa, data=request.data)
#         if serializer.is_valid():
#             serializer.save(sign_a = True)
#             obj = generics.get_object_or_404(workflowitems, id=useraa.workflowitem.id)
#             obj.submit_sign_a()
#             obj.save()
#             # print(self.workflowitem)
#             return Response({"status": "okko", "data": serializer.data},status=status.HTTP_200_OK)
#         return Response({"status": "no "},status=status.HTTP_406_NOT_ACCEPTABLE)



# class SignatureUpdateSign_bApiview(RetrieveUpdateAPIView):
#     queryset = signatures.objects.all()
#     serializer_class = signaturesserializer
    

#     def update(self, request, pk=None):
#         queryset = signatures.objects.all()
#         useraa = get_object_or_404(queryset, pk=pk)
#         print(useraa.workflowitem.id)
#         serializer = signaturesserializer(useraa, data=request.data)
#         if serializer.is_valid():
#             serializer.save(sign_b = True)
#             obj = generics.get_object_or_404(workflowitems, id=useraa.workflowitem.id)
#             obj.submit_sign_b()
#             obj.save()
#             return Response({"status": "ok", "data": serializer.data})
#         return Response({"status": "no "})


# class SignatureUpdateSign_cApiview(RetrieveUpdateAPIView):
#     queryset = signatures.objects.all()
#     serializer_class = signaturesserializer
    

#     def update(self, request, pk=None):
#         queryset = signatures.objects.all()
#         useraa = get_object_or_404(queryset, pk=pk)
#         print(useraa.workflowitem.id)
#         serializer = signaturesserializer(useraa, data=request.data)
#         if serializer.is_valid():
#             serializer.save(sign_c = True)
#             obj = generics.get_object_or_404(workflowitems, id=useraa.workflowitem.id)
#             obj.submit_sign_c()
#             obj.save()
#             # print(self.workflowitem)
#             return Response({"status": "ok", "data": serializer.data})
#         return Response({"status": "no "})