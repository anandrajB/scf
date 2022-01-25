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
from accounts.models import Countries, Currencies, Parties, signatures, userprocessauth
from transaction.models import Programs ,workflowitems
from .serializer import (
    BankSignupSerializer,
    Countriesserializer,
    CurrenciesSerializer,
    GetUserSerilaizer,
    PartiesSignupSerailizer,
    UserSignupSerializer,
    UserSignupSerializer,
    LoginSerializer,
    UserUpdateSerilaizer,
    partieserializer,
    signaturesserializer,
    userprocesserializer,
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


# PARTIES SIGNUP

class PartiesSignupApiview(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = PartiesSignupSerailizer
    permission_classes = [AllowAny]

    def list(self, request):
        queryset = Parties.objects.all()
        serializer = partieserializer(queryset, many=True)
        return Response({"status": "success", "data": serializer.data})

    def post(self, request):
        serializer = PartiesSignupSerailizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success"}, status=status.HTTP_201_CREATED)
        return Response({"status": "failure", "data": serializer.errors})


# USER SIGNUP API 

class UserSignUpApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = [AllowAny]

    

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success"}, status=status.HTTP_201_CREATED)
        return Response({"status": "failure", "data": serializer.errors})


# USER LOGIN API

class UserLoginView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email',None)
        phone = request.data.get("phone", None)
        
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
                    "party" : user.party.name,
                    "display_name": user.display_name,
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


# USER UPDATE API VIEW 
class UserDetailsUpdateDeleteApiview(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerilaizer
    permission_classes = [AllowAny]
    # metadata_class = APIRootMetadata

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserUpdateSerilaizer(user)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserUpdateSerilaizer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "failure", "data": serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)



# USER LOGOUT API 

class UserLogoutView(APIView):
    premission_classes = [IsAuthenticated]

    def post(self, request):
        print("logout")
        logout(request)
        return Response({"status": "logout success"}, status=status.HTTP_200_OK)


# USER LIST API VIEW

class UserListApiview(ListAPIView):
    queryset = User.objects.all()
    serializer_class = GetUserSerilaizer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = User.objects.all()
        serializer = GetUserSerilaizer(queryset, many=True)
        return Response({"status": "success", "data": serializer.data})


# CURRENCIES API VIEW

class CurrenciesView(ListCreateAPIView):
    queryset = Currencies.objects.all()
    serializer_class = CurrenciesSerializer
    permission_classes = [AllowAny]

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


# COUNTRIES API VIEW

class Countriesview(ListCreateAPIView):
    queryset = Countries.objects.all()
    serializer_class = Countriesserializer
    permission_classes = [AllowAny]

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


# HOME PAGE CUSTOM 404 
def index(request):
    return render(request,'index.html')


# SIGNATURES LIST API VIEW
class SignatureList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = signaturesserializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = User.objects.all()
        serializer = signaturesserializer(queryset, many=True)
        return Response({"status": "success", "data": serializer.data},status=status.HTTP_200_OK)



# USER PROCESS API VIEW

class UserProcessView(ListCreateAPIView):
    queryset = userprocessauth.objects.all()
    serializer_class = userprocesserializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = userprocesserializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response({"Status": "Success"},status=status.HTTP_201_CREATED)
        return Response({"Status": "Failed", "data": serializer.errors},status=status.HTTP_406_NOT_ACCEPTABLE)

    def list(self, request):
        model1 = userprocessauth.objects.all()
        serializer = userprocesserializer(model1, many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)



# SIGNATURES LIST CREATE API VIEW

class SignaturesCreateApiView(ListCreateAPIView):
    queryset = signatures.objects.all()
    serializer_class = signaturesserializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = signaturesserializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response({"Status": "Success"},status=status.HTTP_201_CREATED)
        return Response({"Status": "Failed", "data": serializer.errors},status=status.HTTP_406_NOT_ACCEPTABLE)

    def list(self, request):
        model1 = signatures.objects.all().order_by('id')
        mode2 = signatures.objects.filter(action = 'SUBMIT',type = 1).values_list('id',flat=True).first()
        print("the value is",mode2)
        serializer = signaturesserializer(model1, many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)
