from .models import ProgramType, Programs
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.generics import ListAPIView ,ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .serializer import  ProgramSerializer , ProgramTypeserilaizer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.permissions import AllowAny , AllowAny
from django.shortcuts import get_object_or_404



class programtypelistapiview(ListCreateAPIView):
    queryset = ProgramType.objects.all()
    serializer_class = ProgramTypeserilaizer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProgramTypeserilaizer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProgramTypeserilaizer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response({"Status": "Success"})
        return Response({"Status": "Failed", "data": serializer.errors})


class ProgramtypeupdateDeleteapiview(RetrieveUpdateDestroyAPIView):
    queryset = ProgramType.objects.all()
    serializer_class = ProgramTypeserilaizer
    permission_classes = [AllowAny]

    def retrieve(self, request, pk=None):
        queryset = ProgramType.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ProgramTypeserilaizer(user)
        return Response({"status": "success", "data": serializer.data})

    def update(self, request, pk=None):
        queryset = ProgramType.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ProgramTypeserilaizer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response({"status": "failure", "data": serializer.errors})




class ProgramListApiview(ListAPIView):
    queryset = Programs.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProgramSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProgramSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response({"Status": "Success"})
        return Response({"Status": "Failed", "data": serializer.errors})

class ProgramupdateDeleteapiview(RetrieveUpdateDestroyAPIView):
    queryset = Programs.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [AllowAny]

    def retrieve(self, request, pk=None):
        queryset = Programs.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ProgramSerializer(user)
        return Response({"status": "success", "data": serializer.data})

    def update(self, request, pk=None):
        queryset = Programs.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ProgramSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response({"status": "failure", "data": serializer.errors})