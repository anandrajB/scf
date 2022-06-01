import random
import http.client
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from accounts.models import (
    Action,
    Banks, 
    Countries, 
    Currencies,
    Models, 
    Parties, 
    PhoneOTP, 
    signatures, 
    userprocessauth
)
from accounts.email import email_to
from .serializer import (
    Actionserializer,
    BankSerializer,
    Countriesserializer,
    CurrenciesSerializer,
    GetUserSerilaizer,
    Modelserializer,
    Otpserializer,
    PartiesSignupSerailizer,
    UserSignupSerializer,
    UserSignupSerializer,
    LoginSerializer,
    UserUpdateSerilaizer,
    Userprocessserialzier,
    partieserializer,
    signaturecreateserializer,
    signatureslistserializer,
    userprocesscreateserializer,
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



# CONNECTION FOR OTP 
conn = http.client.HTTPConnection("2factor.in")


# MYUSER MODEL
User = get_user_model()


# API END POINTS PAGE
def endpoint(request):
    return render(request,'apiend.html')


# HOME PAGE  
def index(request):
    return render(request,'index.html')


# CUSTOM 404 PAGE ( USE IN PRODUCTION  )
def error_404_view(request, exception):
    return render(request,'404.html')


# CUSTOM 404 PAGE ( USE IN PRODUCTION  )
def error_500_view(request, *args, **argv):
    return render(request,'500.html')



#function for random otp - 6 digit
def generate_otp(phone):
    key = random.randint(100000,999999)
    return key


# BANK CREATE

class BankCreateApiview(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = BankSerializer
    permission_classes = [AllowAny]

    def list(self, request):
        queryset = Banks.objects.all()
        serializer = BankSerializer(queryset, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BankSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "failure", "data": serializer.errors}, status =status.HTTP_204_NO_CONTENT)


# PARTIES CREATE


class PartiesSignupApiview(ListAPIView):
    queryset = Parties.objects.all()
    serializer_class = PartiesSignupSerailizer
    permission_classes = [AllowAny]
    

    def list(self, request):
        queryset = Parties.objects.all()
        serializer = partieserializer(queryset, many=True)
        return Response({"status": "success", "data": serializer.data},status=status.HTTP_200_OK)
    

    def post(self, request):
        serializer = PartiesSignupSerailizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success","data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "failure", "data": serializer.errors},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


# PARTY UPDATE API VIEW

class PartyDetailsUpdateDeleteApiview(RetrieveUpdateDestroyAPIView):
    queryset = Parties.objects.all()
    serializer_class = partieserializer
    permission_classes = [AllowAny]

    def retrieve(self, request, pk=None):
        queryset = Parties.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = partieserializer(user)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        queryset = Parties.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = partieserializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "failure", "data": serializer.errors}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)



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
        return Response({"status": "failure", "data": serializer.errors},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


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
                if user.is_active == False:
                    return Response({"status": "failure", "data": "This user is_inactive , please contact customer support team finflosupport@xyz.com"},status = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
                else:
                    login(request, user)
                    token, created = Token.objects.get_or_create(user=user)
                    data = {
                        "user_id": user.id,
                        "token": token.key,
                        "phone": user.phone,
                        "email": user.email,
                        "party" : user.party.name,
                        "party_type" : user.party.party_type,
                        "party_id": user.party.id,
                        "display_name": user.display_name,
                        "is_active" : user.is_active,
                        "is_administrator" : user.is_administrator,
                        "is_supervisor" : user.is_supervisor,
                        'is_master_admin' : user.is_master_admin,
                    }
                    return Response({"status": "success", "data": data }, status=status.HTTP_200_OK)
            return Response(
                {"status": "failure", "data": "Unable to login with given credentials"} , status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
            )
        return Response(
            {
                "status": "failure",
                "data": "You need to provide both phone and email",
            }, status=status.HTTP_204_NO_CONTENT
        )


# USER LOGIN OTP GENERATE

class OtpSendApi(APIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email',None)
        phone = request.data.get("phone", None)
        
        if phone and email:
            user = User.objects.filter(phone = phone , email = email).exists()
            if user:
                key = generate_otp(phone)
                otp_gen = PhoneOTP.objects.create(email = email , phone = phone , otp = key )
                otp_gen.save() 
                email_to(email,key)
                conn.request("GET", "https://2factor.in/API/R1/?module=SMS_OTP&apikey=48ec2bf6-8251-11ec-b9b5-0200cd936042&to="+phone+"&otpvalue="+str(key)+"&templatename=FINFLO")
                res = conn.getresponse() 
                return Response({"status": "success", "data": "otp sent to your phone and email "}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "failure", "data": "given details doesn't exists"}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        return Response(
            {
                "status": "failure",
                "data": "You need to provide both phone and email",
            },status=status.HTTP_204_NO_CONTENT
        )


# OTP VERIFY AND LOGIN 

class OtpVerifyLoginApiview(APIView):
    queryset = User.objects.all()
    serializer_class = Otpserializer
    permission_classes = [AllowAny]


    def post(self, request):
        email = self.request.query_params.get("email", None)
        phone = self.request.query_params.get("phone", None)
        OTP  = request.data.get("otp", None)

        if phone and email:
            user = authenticate(phone=phone,email=email)
            usergg = PhoneOTP.objects.filter(email = email)
            cc = usergg.last()
            
            if user and str(cc.otp) == OTP:
                if user.is_active == False:
                    return Response({"status": "failure", "data": "This user is_inactive , please contact customer support team venzo@xyz.com"},status = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
                else:
                    login(request, user)
                    token, created = Token.objects.get_or_create(user=user)
                    data = {
                        "user_id": user.id,
                        "token": token.key,
                        "phone": user.phone,
                        "email": user.email,
                        "party" : user.party.name,
                        "party_type" : user.party.party_type,
                        "party_id": user.party.id,
                        "display_name": user.display_name,
                        "is_active" : user.is_active,
                        "is_administrator" : user.is_administrator,
                        "is_supervisor" : user.is_supervisor,
                        'is_master_admin' : user.is_master_admin
                    }
                    return Response({"status": "success", "data": data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "failure", "data": "Wrong OTP "},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        return Response(
            {
                "status": "failure",
                "data": "You should enter a valid 6 digit number",
            },status=status.HTTP_204_NO_CONTENT
        )



# USER LIST API VIEW 

class UserListApiview(ListAPIView):
    queryset = User.objects.all()
    serializer_class = GetUserSerilaizer
    permission_classes = [IsAuthenticated]


    def get_queryset(self,request):
        queryset = User.objects.all()
        user = request.user
        if user.is_administrator == True:
            queryset = User.objects.filter(party = user.party).exclude(id = user.id)
        else:
            queryset = User.objects.filter(email = user.email)
        return queryset

    def list(self, request):
        queryset = self.get_queryset(request)
        serializer = GetUserSerilaizer(queryset, many=True)
        return Response({"status": "success", "data": serializer.data},status = status.HTTP_200_OK)



# USER UPDATE API VIEW 

class UserDetailsUpdateDeleteApiview(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerilaizer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserUpdateSerilaizer(user)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserUpdateSerilaizer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "failure", "data": serializer.errors}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)



# USER LOGOUT API 

class UserLogoutView(APIView):
    premission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"status": "logout success"}, status=status.HTTP_200_OK)



# USER PROFILE API VIEW

class UserProfileApiView(ListAPIView):
    queryset = User.objects.all()
    serilizer_class = GetUserSerilaizer
    permission_classes = [IsAuthenticated]

    def list(self,request):
        user = request.user
        query = User.objects.filter(id = user.id)
        serializer = GetUserSerilaizer(query,many=True)
        return Response({"status": "success", "data": serializer.data},status=status.HTTP_200_OK)


# CURRENCIES API VIEW

class CurrenciesView(ListCreateAPIView):
    queryset = Currencies.objects.all()
    serializer_class = CurrenciesSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CurrenciesSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response({"status": "success", "data": serializer.data},status=status.HTTP_201_CREATED)
        return Response({"Status": "Failed", "data": serializer.errors},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    def list(self, request):
        model1 = Currencies.objects.all()
        serializer = CurrenciesSerializer(model1, many=True)
        return Response({"status": "success", "data": serializer.data},status=status.HTTP_200_OK)


# CURRENCIES UPDATE API VIEW 

class CurrenciesUpdateDeleteApiview(RetrieveUpdateDestroyAPIView):
    queryset = Currencies.objects.all()
    serializer_class = CurrenciesSerializer
    permission_classes = [IsAuthenticated]
   
    def retrieve(self, request, pk=None):
        queryset = Currencies.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = CurrenciesSerializer(user)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        queryset = Currencies.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = CurrenciesSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "successfully changed", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "failure", "data": serializer.errors}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)



# COUNTRIES LIST  API VIEW

class CountriesApiView(ListCreateAPIView):
    queryset = Countries.objects.all()
    serializer_class = Countriesserializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = Countriesserializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response({"status": "success", "data": serializer.data},status=status.HTTP_201_CREATED)
        return Response({"Status": "Failed", "data": serializer.errors},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    def get(self, request):
        model1 = Countries.objects.all()
        serializer = Countriesserializer(model1, many=True)
        return Response({"Status": "success", "data": serializer.data},status=status.HTTP_200_OK)


# COUNTRIES UPDATE API VIEW 

class CountryUpdateDeleteApiview(RetrieveUpdateDestroyAPIView):
    queryset = Countries.objects.all()
    serializer_class = Countriesserializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        queryset = Countries.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = Countriesserializer(user)
        return Response({"Status": "Success", "data": serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        queryset = Countries.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = Countriesserializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Status": "successfully updated", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"Status": "Failure", "data": serializer.errors}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)




# USER PROCESS API VIEW

class UserProcessAuthView(ListCreateAPIView):
    queryset = userprocessauth.objects.all()
    serializer_class = userprocesscreateserializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user  =  self.request.user
        serializer = userprocesscreateserializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user = user)
            return Response({"Status": "Success", "data":serializer.data},status=status.HTTP_201_CREATED)
        return Response({"Status": "Failure", "data": serializer.errors},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    def list(self, request):
        user = self.request.user
        model1 = userprocessauth.objects.filter(user = user)
        serializer = Userprocessserialzier(model1, many=True)
        return Response({"Status": "Success", "data":serializer.data},status=status.HTTP_200_OK)


# USER PROCESS UPDATE API VIEW

class UserProcessAuthUpdateApiview(RetrieveUpdateDestroyAPIView):
    queryset = userprocessauth.objects.all()
    serializer_class = userprocesscreateserializer
    permission_classes = [IsAuthenticated]
   
    def retrieve(self, request, pk=None):
        queryset = userprocessauth.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = userprocesscreateserializer(user)
        return Response({"Status": "Success", "data": serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        queryset = userprocessauth.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = userprocesscreateserializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response({"Status": "successfully updated", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"Status": "Failure", "data": serializer.errors}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)



# SIGNATURES LIST CREATE API VIEW

class SignaturesCreateApiView(ListCreateAPIView):
    queryset = signatures.objects.all()
    serializer_class = signaturecreateserializer
    permission_classes = [IsAuthenticated]

    
    def post(self, request):
        serializer = signaturecreateserializer(data=request.data)
        party = request.user.party
        if(serializer.is_valid()):
            serializer.save(party = party)
            return Response({"Status": "Success", "data": serializer.data},status=status.HTTP_201_CREATED)
        return Response({"Status": "Failure", "data": serializer.errors},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    def list(self, request):
        user = request.user
        queryset = signatures.objects.filter(party=user.party)
        serializer = signatureslistserializer(queryset, many=True)
        return Response({"status": "success", "data": serializer.data},status=status.HTTP_200_OK)



# SIGNATURES UPDATE API VIEW 

class SignaturesUpdateDeleteApiview(RetrieveUpdateDestroyAPIView):
    queryset = signatures.objects.all()
    serializer_class = signaturecreateserializer
    permission_classes = [IsAuthenticated]
   
    def retrieve(self, request, pk=None):
        queryset = signatures.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = signaturecreateserializer(user)
        return Response({"Status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        queryset = signatures.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = signaturecreateserializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Status": "successfully updated", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"Status": "Failure", "data": serializer.errors}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


# ACTION CREATE API 

class ActionApiview(ListCreateAPIView):
    queryset = Action.objects.all()
    serializer_class = Actionserializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = Action.objects.all()
        serializer = Actionserializer(queryset, many=True)
        return Response({"Status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = Actionserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"Status": "Failure", "data": serializer.errors}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)



# ACTION UPDATE API VIEW 

class ActionUpdateDeleteApiview(RetrieveUpdateDestroyAPIView):
    queryset = Action.objects.all()
    serializer_class = Actionserializer
    permission_classes = [IsAuthenticated ]

    def retrieve(self, request, pk=None):
        queryset = Action.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = Actionserializer(user)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        queryset = Action.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = Actionserializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "successfully updated", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "Failure", "data": serializer.errors}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


# MODEL CREATE API VIEW

class ModelApiview(ListCreateAPIView):
    queryset = Models.objects.all()
    serializer_class = Modelserializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = Models.objects.all()
        serializer = Modelserializer(queryset, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = Modelserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "Failure", "data": serializer.errors},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


# MODEL UPDATE API VIEW 

class ModelUpdateDeleteApiview(RetrieveUpdateDestroyAPIView):
    queryset = Models.objects.all()
    serializer_class = Modelserializer
    permission_classes = [IsAuthenticated]
   
    def retrieve(self, request, pk=None):
        queryset = Models.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = Modelserializer(user)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        queryset = Models.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = Modelserializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "successfully updated", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "Failed", "data": serializer.errors}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
