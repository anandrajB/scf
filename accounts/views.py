from datetime import datetime
import random
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
)
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from accounts.models import Countries, Currencies, signatures
from transaction.models import Programs ,workflowitems
from .serializer import (
    BankSignupSerializer,
    Countriesserializer,
    CurrenciesSerializer,
    CustomerSerializer,
    GetUserSerilaizer,
    PartiesSignupSerailizer,
    CustomerSignupSerializer,
    LoginSerializer,
    signaturesserializer,
)
from django.contrib.auth import (
    get_user_model,
    authenticate,
    login,
    logout
)
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

class BankCreateApiview(CreateAPIView):
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
        phone = request.data.get("phone", None)
        email = request.data.get('email',None)
        if phone and email:
            user = authenticate(phone=phone,email=email)
            if user:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                data = {
                    "id": user.id,
                    "token": token.key,
                    "phone": user.phone,
                    "email": user.email,
                    "is_administrator" : user.is_administrator,
                    "is_supervisor" : user.is_supervisor
                }
                return Response({"status": "success", "data": data}, status=status.HTTP_200_OK)
            return Response(
                {"status": "failure", "data": "Unable to login with given credidentials"}
            )
        return Response(
            {
                "status": "failure",
                "data": "You need to provide both phone and email",
            }
        )


class UserLogoutView(APIView):
    premission_classes = [IsAuthenticated]

    def post(self, request):
        print("logout")
        logout(request)
        return Response({"status": "logout success"}, status=status.HTTP_200_OK)


class CustomerListApiview(ListAPIView):
    queryset = User.objects.all()
    serializer_class = GetUserSerilaizer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = User.objects.all()
        serializer = GetUserSerilaizer(queryset, many=True)
        return Response({"status": "success", "data": serializer.data})

class CurrenciesView(ListCreateAPIView):
    queryset = Currencies.objects.all()
    serializer_class = CurrenciesSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CurrenciesSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response({"Status": "Success"},status=status.HTTP_201_CREATED)
        return Response({"Status": "Failed", "data": serializer.errors},status=status.HTTP_406_NOT_ACCEPTABLE)

    def list(self, request):
        model1 = Currencies.objects.all()
        serializer = CurrenciesSerializer(model1, many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)


class Countriesview(ListCreateAPIView):
    queryset = Countries.objects.all()
    serializer_class = Countriesserializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = Countriesserializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response({"Status": "Success"},status=status.HTTP_201_CREATED)
        return Response({"Status": "Failed", "data": serializer.errors},status=status.HTTP_406_NOT_ACCEPTABLE)

    def get(self, request):
        model1 = Countries.objects.all()
        serializer = Countriesserializer(model1, many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)

def index(request):
    return render(request,'index.html')



class SignatureList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = signaturesserializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = User.objects.all()
        serializer = signaturesserializer(queryset, many=True)
        return Response({"status": "success", "data": serializer.data},status=status.HTTP_200_OK)




class SignatureUpdateApiview(RetrieveUpdateAPIView):
    queryset = signatures.objects.all()
    serializer_class = signaturesserializer
    

    def update(self, request, pk=None):
        queryset = signatures.objects.all()
        useraa = get_object_or_404(queryset, pk=pk)
        print(useraa.workflowitem.id)
        serializer = signaturesserializer(useraa, data=request.data)
        if serializer.is_valid():
            serializer.save(sign_a = True)
            obj = generics.get_object_or_404(workflowitems, id=useraa.workflowitem.id)
            obj.submit_sign_a()
            obj.save()
            # print(self.workflowitem)
            return Response({"status": "okko", "data": serializer.data},status=status.HTTP_200_OK)
        return Response({"status": "no "},status=status.HTTP_406_NOT_ACCEPTABLE)



class SignatureUpdateSign_bApiview(RetrieveUpdateAPIView):
    queryset = signatures.objects.all()
    serializer_class = signaturesserializer
    

    def update(self, request, pk=None):
        queryset = signatures.objects.all()
        useraa = get_object_or_404(queryset, pk=pk)
        print(useraa.workflowitem.id)
        serializer = signaturesserializer(useraa, data=request.data)
        if serializer.is_valid():
            serializer.save(sign_b = True)
            obj = generics.get_object_or_404(workflowitems, id=useraa.workflowitem.id)
            obj.submit_sign_b()
            obj.save()
            return Response({"status": "ok", "data": serializer.data})
        return Response({"status": "no "})


class SignatureUpdateSign_cApiview(RetrieveUpdateAPIView):
    queryset = signatures.objects.all()
    serializer_class = signaturesserializer
    

    def update(self, request, pk=None):
        queryset = signatures.objects.all()
        useraa = get_object_or_404(queryset, pk=pk)
        print(useraa.workflowitem.id)
        serializer = signaturesserializer(useraa, data=request.data)
        if serializer.is_valid():
            serializer.save(sign_c = True)
            obj = generics.get_object_or_404(workflowitems, id=useraa.workflowitem.id)
            obj.submit_sign_c()
            obj.save()
            # print(self.workflowitem)
            return Response({"status": "ok", "data": serializer.data})
        return Response({"status": "no "})



