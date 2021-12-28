from accounts.models import workevents
from .models import Programs
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.generics import ListAPIView , CreateAPIView ,ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .serializer import ProgramListserializer , Programcreateserializer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.permissions import AllowAny , AllowAny
from django.shortcuts import get_object_or_404
from rest_framework import status


# class ProgramupdateDeleteapiview(RetrieveUpdateDestroyAPIView):
#     queryset = Programs.objects.all()
#     serializer_class = ProgramSerializer
#     permission_classes = [AllowAny]

#     def retrieve(self, request, pk=None):
#         queryset = Programs.objects.all()
#         user = get_object_or_404(queryset, pk=pk)
#         serializer = ProgramSerializer(user)
#         return Response({"status": "success", "data": serializer.data})

#     def update(self, request, pk=None):
#         queryset = Programs.objects.all()
#         user = get_object_or_404(queryset, pk=pk)
#         serializer = ProgramSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"status": "success", "data": serializer.data})
#         return Response({"status": "failure", "data": serializer.errors})


class Proslistapiview(ListAPIView):
    queryset = Programs.objects.all()
    serializer_class = ProgramListserializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProgramListserializer(queryset, many=True)
        return Response(serializer.data)


class Proscreateapiview(CreateAPIView):
    queryset = Programs.objects.all()
    serializer_class = Programcreateserializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = Programcreateserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success"}, status=status.HTTP_201_CREATED)
        return Response({"status": "failure", "data": serializer.errors})


class ProgramupdateDeleteapiview(RetrieveUpdateDestroyAPIView):
    queryset = Programs.objects.all()
    serializer_class = ProgramListserializer
    permission_classes = [AllowAny]

    def retrieve(self, request, pk=None):
        queryset = Programs.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ProgramListserializer(user)
        return Response({"status": "success", "data": serializer.data})

    def update(self, request, pk=None):
        queryset = Programs.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ProgramListserializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response({"status": "failure", "data": serializer.errors})


