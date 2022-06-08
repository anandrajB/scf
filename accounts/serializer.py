from django.contrib.auth import get_user_model
from .models import (
    Action,
    Banks, 
    Countries,
    Currencies,
    Parties, 
    PhoneOTP, 
    signatures, 
    userprocessauth,
    Models
)  
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.conf import settings
from rest_framework.validators import UniqueTogetherValidator


# MY USER MODEL
User = get_user_model()



# OTP SERIALIZER 

class Otpserializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneOTP
        fields = ['otp']

        
# BANK SERIALIZER

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banks
        fields = '__all__'
    
    def validate_name(self, attrs):
        if Banks.objects.filter(name= attrs).exists():
            raise serializers.ValidationError("bank name already exists")
        return attrs


# PARTY LIST SERIALIZER

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


# PARTY SIGNUP SERIALIZERS

class PartiesSignupSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Parties
        fields = '__all__'
        extra_kwargs = {
		"address_line_1": {"required": False},
        "address_line_2": {"required": False},
        "city": {"required": False},
        "state": {"required": False},
        "zipcode": {"required": False},
	}
    # validators = [UniqueTogetherValidator(queryset=Parties.objects.all(),fields=['customer_id', 'name'])]
    def validate_customer_id(self,value):
        if Parties.objects.filter(customer_id = value).exists():
            raise serializers.ValidationError("A party with this customer_id  already exists , try with other customer_id")
        return value

    def validate_name(self,value):
        if Parties.objects.filter(name = value).exists():
            raise serializers.ValidationError("A party with this name already exists , try with other name")
        return value

    
        

# USER SIGNUP SERIALIZER 

class UserSignupSerializer(serializers.Serializer):
    email = serializers.CharField(required = False)
    phone = serializers.CharField(required = False)
    party = serializers.PrimaryKeyRelatedField(queryset = Parties.objects.all())
    first_name = serializers.CharField(required = False)
    last_name = serializers.CharField(required = False)
    display_name = serializers.CharField(required = False)
    supervisor = serializers.BooleanField(required = False)
    administrator = serializers.BooleanField(required = False)
    profile_picture = serializers.FileField(required = False)

    
    def create(self, validated_data):
        email = validated_data.pop('email')
        phone = validated_data.pop('phone')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        display_name = validated_data.pop('display_name')
        profile_picture = validated_data.pop('profile_picture')
        party = validated_data.pop('party')
        supervisor = validated_data.pop('supervisor')
        administrator = validated_data.pop('administrator')
    
        user = User.objects.create(phone = phone , email = email ,first_name = first_name ,  last_name =last_name, profile_img = profile_picture,display_name = display_name , party = party,  is_supervisor = supervisor , is_administrator = administrator )
        user.save()
        return user
        

    def validate_email(self,value):
        if User.objects.filter(email = value).exists():
            raise serializers.ValidationError("user with this email_id already exists")
        return value
        
    def validate_phone(self, attrs):
        if User.objects.filter(phone = attrs).exists():
            raise serializers.ValidationError("user with this phone number already exists")
        return attrs

    
# LOGIN SERIALIZER

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email","phone"]



# GET USER SERIALIZER

class GetUserSerilaizer(serializers.ModelSerializer):
    party = serializers.SlugRelatedField(read_only = True , slug_field= 'name')
    class Meta:
        model = User
        fields = [
            "id",
            "last_login",
            "phone",
            "email",
            "display_name",
            "first_name",
            "last_name",
            'party',
            'profile_img',
            'is_active',
            "is_supervisor",
            "is_administrator",
            "created_date",
        ]

    
# USER UPDATE SERIALIZER 

class UserUpdateSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'phone',
            'email',
            'first_name',
            'last_name',
            'display_name',
            'profile_img',
            'party',
            'is_active',
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



class Actionserializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'


class Modelserializer(serializers.ModelSerializer):
    class Meta:
        model = Models
        fields = '__all__'



class signatureslistserializer(serializers.ModelSerializer):
    action = serializers.SlugRelatedField(read_only = True ,slug_field='desc')
    party = serializers.SlugRelatedField(read_only = True , slug_field= 'name')
    class Meta:
        model = signatures
        fields = [
            'id',
            'model',
            'action',
            'party',
            'sign_a',
            'sign_b',
            'sign_c'
        ]


class signaturecreateserializer(serializers.ModelSerializer):
    class Meta:
        model = signatures
        fields = '__all__'


class Userprocessserialzier(serializers.ModelSerializer):
    action = serializers.SlugRelatedField(read_only = True ,slug_field='desc')
    class Meta:
        model = userprocessauth
        fields = [
            'id',
            'user',
            'model',
            'action',
            'data_entry',
            'sign_a',
            'sign_b',
            'sign_c'
        ]



class userprocesscreateserializer(serializers.ModelSerializer):
    action = serializers.PrimaryKeyRelatedField(queryset=Action.objects.all())
    class Meta:
        model = userprocessauth
        fields = [
            'id',
            'model',
            'action',
            'user',
            'data_entry',
            'sign_a',
            'sign_b',
            'sign_c'
        ]

