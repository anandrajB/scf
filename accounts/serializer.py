from django.contrib.auth import get_user_model

from transaction.models import submodels
from .models import Banks, Countries, Currencies, Parties, PhoneOTP, signatures, userprocessauth  
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.conf import settings
from django.core.mail import EmailMessage
import time


User = get_user_model()


# EMAIL FUNCTION FOR EMAIL OTP
def email_to(to_email,key):
    
    subject = "OTP for Finflo Login "

    message = """Dear {0} ,  your otp to login is {1} """.format(str(to_email),str(key))

    email_from = settings.EMAIL_HOST_USER
    recipient_list = [to_email]
    cc_list = ["anand98.ar@gmail.com"]

    email = EmailMessage(
        subject,
        message,
        email_from,
        recipient_list,
        cc_list,
    )
    email.send(fail_silently=False)



# OTP SERIALIZER 

class Otpserializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneOTP
        fields = ['otp']

        
# SERIALIZER'S 

class BankListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banks
        fields = '__all__'


class BankSignupSerializer(serializers.Serializer):
    name = serializers.CharField()
    address_line_1 = serializers.CharField()
    address_line_2 = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()
    zipcode = serializers.CharField()
    country_code = serializers.PrimaryKeyRelatedField(queryset = Countries.objects.all())

    def create(self, validated_data):
        name = validated_data.pop("name")
        country_code = validated_data.pop("country_code")
        address_line_1 = validated_data.pop("address_line_1")
        address_line_2 = validated_data.pop('address_line_2')
        city = validated_data.pop('city')
        state = validated_data.pop('state')
        zipcode = validated_data.pop('zipcode')
        bank = Banks.objects.create(name = name , address_line_1 = address_line_1 , address_line_2 = address_line_2 , city = city ,state = state, zipcode = zipcode , country_code = country_code)
        return bank

    def validate_name(self, attrs):
        if Banks.objects.filter(name= attrs).exists():
            raise serializers.ValidationError("bank name already exists")
        return attrs


class partieserializer(serializers.ModelSerializer):
    country_code = serializers.SlugRelatedField(read_only=True, slug_field='country')
    base_currency = serializers.SlugRelatedField(read_only=True, slug_field='description')
    class Meta:
        model = Parties
        fields = [
            'id',
            'name',
            'customer_id',
            'address_line_1',
            'address_line_2',
            'onboarded',
            'party_type',
            'city',
            'base_currency',
            'state',
            'zipcode',
            'country_code',
            'party_type'
        ]



class PartiesSignupSerailizer(serializers.Serializer):

    party_type_choices = [
    ('CUSTOMER','CUSTOMER'),
    ('BANK','BANK'),
    ('OTHER','OTHER')
    ]

    name = serializers.CharField()
    customer_id = serializers.CharField()
    country_code = serializers.PrimaryKeyRelatedField(queryset = Countries.objects.all())
    name = serializers.CharField()
    base_currency = serializers.PrimaryKeyRelatedField(queryset = Currencies.objects.all())
    party_type = serializers.ChoiceField(choices=party_type_choices)
    address_1 = serializers.CharField()
    on_boarded = serializers.BooleanField()
    address_2 = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()
    zipcode = serializers.CharField()

    def create(self, validated_data):
        party_type = validated_data.pop("party_type")
        name = validated_data.pop('name')
        country_code = validated_data.pop("country_code")
        customer_user_id = validated_data.pop('customer_id')
        base_currency = validated_data.pop("base_currency")
        address_1 = validated_data.pop("address_1")
        address_2 = validated_data.pop('address_2')
        city = validated_data.pop('city')
        state = validated_data.pop('state')
        on_boarded = validated_data.pop('on_boarded')
        zipcode = validated_data.pop('zipcode')
        party = Parties.objects.create(
            party_type = party_type  ,onboarded = on_boarded,state = state,country_code = country_code ,customer_id = customer_user_id , name = name ,base_currency = base_currency , address_line_1 = address_1 , address_line_2 = address_2 , city = city , zipcode =zipcode
        )
        return party


    def validate_customer_id(self,value):
        if Parties.objects.filter(customer_id = value).exists():
            raise serializers.ValidationError("A party with this customer_id / account already exists , try another customer_id")
        return value
        

    


class UserSignupSerializer(serializers.Serializer):
    email = serializers.CharField()
    phone = serializers.CharField()
    party = serializers.PrimaryKeyRelatedField(queryset = Parties.objects.all())
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    display_name = serializers.CharField()
    maker = serializers.BooleanField()
    sign_a = serializers.BooleanField()
    sign_b = serializers.BooleanField()
    sign_c = serializers.BooleanField()
    supervisor = serializers.BooleanField()
    administrator = serializers.BooleanField()
    
    def create(self, validated_data):
        email = validated_data.pop('email')
        phone = validated_data.pop('phone')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        display_name = validated_data.pop('display_name')
        party = validated_data.pop('party')
        maker = validated_data.pop('maker')
        sign_a = validated_data.pop('sign_a')
        sign_b = validated_data.pop('sign_b')
        sign_c = validated_data.pop('sign_c')
        supervisor = validated_data.pop('supervisor')
        administrator = validated_data.pop('administrator')
        user = User.objects.create(phone = phone , email = email ,first_name = first_name ,  last_name =last_name ,display_name = display_name , party = party, is_maker = maker , is_sign_a = sign_a , is_sign_b = sign_b , is_sign_c = sign_c, is_supervisor = supervisor , is_administrator = administrator )
        user.save()
        return user

    def validate_email(self,value):
        if User.objects.filter(email = value).exists():
            raise serializers.ValidationError("user with this email_id already exists")
        return value
        
    def validate_phone(self, attrs):
        if User.objects.filter(phone = attrs).exists():
            raise serializers.ValidationError("user with this phone number already exits")
        return attrs

    

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email","phone"]



class GetUserSerilaizer(serializers.ModelSerializer):
    party = serializers.SlugRelatedField(read_only = True , slug_field= 'name')
    class Meta:
        model = User
        fields = [
            "id",
            "password",
            "last_login",
            "phone",
            "email",
            "display_name",
            "first_name",
            "last_name",
            'party',
            'is_active',
            'is_maker',
            'is_sign_a',
            'is_sign_b',
            'is_sign_c',
            "is_supervisor",
            "is_administrator",
            "created_date",
        ]
        extra_kwargs = {"password": {"write_only": True}}
        read_only_fields = [
            "id",
            "last_login",
            "date_joined",
        ]

    def create(self, validated_data):
        user = super(GetUserSerilaizer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserUpdateSerilaizer(serializers.ModelSerializer):
    # party = serializers.SlugRelatedField(read_only = True , slug_field='name')
    class Meta:
        model = User
        fields = [
            'phone',
            'email',
            'first_name',
            'last_name',
            'display_name',
            'party',
            'is_maker',
            'is_sign_a',
            'is_sign_b',
            'is_sign_c',
            'is_supervisor',
            'is_administrator',
            'created_date',
            'last_login',
        ]


class CurrenciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currencies
        fields = '__all__'


class Countriesserializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        fields = '__all__'




class signaturesserializer(serializers.ModelSerializer):
    party = serializers.SlugRelatedField(read_only = True , slug_field= 'name')
    class Meta:
        model = signatures
        fields = [
            'model',
            'action',
            'party',
            'sign_a',
            'sign_b',
            'sign_c'
        ]


class Userprocessserialzier(serializers.ModelSerializer):
    signature = signaturesserializer(read_only=True)
    class Meta:
        model = userprocessauth
        fields = [
            'id',
            'action',
            'data_entry',
            'sign_a',
            'sign_b',
            'sign_c',
            'user',
            'model_id',
            'signature'
        ]
        read_only_fields = ['signature']
    

class signaturescreateserializer(serializers.Serializer):
    model = serializers.CharField()
    action = serializers.CharField()
    party = serializers.PrimaryKeyRelatedField(queryset = Parties.objects.all())
    sign_a = serializers.BooleanField()
    sign_b = serializers.BooleanField()
    sign_c = serializers.BooleanField()
    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all())

    def create(self, validated_data):
        model = validated_data.pop('model')
        action = validated_data.pop('action')
        party = validated_data.pop('party')
        sign_a = validated_data.pop('sign_a')
        sign_b = validated_data.pop('sign_b')
        sign_c = validated_data.pop('sign_c')
        user = validated_data.pop('user')
        signs  = signatures.objects.create( model = model , action = action ,  party = party , sign_a = sign_a , sign_b = sign_b , sign_c = sign_c )
        signs.save()
        process = userprocessauth.objects.create(user = user ,model_id = model , action = action , signature = signs) 
        process.save()
        return signs