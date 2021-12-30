import random
from datetime import datetime
from django.shortcuts import render
from rest_framework import status
from rest_framework import response
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from accounts.models import Countries, Currencies
from transaction.models import Programs
from .serializer import (
    BankSignupSerializer,
    Countriesserializer,
    CurrenciesSerializer,
    CustomerSerializer,
    GetUserSerilaizer,
    PartiesSignupSerailizer,
    CustomerSignupSerializer,
    LoginSerializer,
)
from django.contrib.auth import get_user_model, authenticate, login, logout
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
)
from rest_framework.response import Response

User = get_user_model()

# Create your views here.


#function for random otp 
def generate_code():
    from_range = 000000
    to_range = 999999
    return random.randint(from_range, to_range)

class BankSignupApiview(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = BankSignupSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = BankSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success"}, status=status.HTTP_201_CREATED)
        return Response({"status": "failure", "data": serializer.errors})


class PartiesSignupApiview(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = PartiesSignupSerailizer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PartiesSignupSerailizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success"}, status=status.HTTP_201_CREATED)
        return Response({"status": "failure", "data": serializer.errors})


class CustomerSignupApiview(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomerSignupSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomerSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success"}, status=status.HTTP_201_CREATED)
        return Response({"status": "failure", "data": serializer.errors})


class UserLoginView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("phone", None)
        password = request.data.get("password", None)
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                data = {
                    "id": user.id,
                    "token": token.key,
                    "phone": user.username,
                    "email": user.email,
                    "first_name" : user.first_name,
                    "last_name " :  user.last_name,
                    "user_type" : user.user_type,
                }
                return Response({"status": "success", "data": data}, status=status.HTTP_200_OK)
            return Response(
                {"status": "failure", "data": "Unable to login with given credidential"}
            )
        return Response(
            {
                "status": "failure",
                "data": "You need to provide both username and password",
            }
        )


class UserLogoutView(APIView):
    premission_classes = [IsAuthenticated]

    def post(self, request):
        print("logout")
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomerListApiview(ListAPIView):
    queryset = User.objects.all()
    serializer_class = GetUserSerilaizer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = User.objects.filter(user_type = 3)
        serializer = GetUserSerilaizer(queryset, many=True)
        return Response({"status": "success", "data": serializer.data})

class CurrenciesView(ListCreateAPIView):
    queryset = Currencies.objects.all()
    serializer_class = CurrenciesSerializer

    def post(self, request):
        serializer = CurrenciesSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response({"Status": "Success"})
        return Response({"Status": "Failed", "data": serializer.errors})

    def get(self, request):
        model1 = Currencies.objects.all()
        serializer = CurrenciesSerializer(model1, many=True)
        return Response(serializer.data)


class Countriesview(ListCreateAPIView):
    queryset = Countries.objects.all()
    serializer_class = Countriesserializer

    def post(self, request):
        serializer = Countriesserializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response({"Status": "Success"})
        return Response({"Status": "Failed", "data": serializer.errors})

    def get(self, request):
        model1 = Countries.objects.all()
        serializer = Countriesserializer(model1, many=True)
        return Response(serializer.data)

def index(request):
    return render(request,'index.html')



