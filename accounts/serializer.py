from django.contrib.auth import get_user_model
from django.contrib.auth import models
from django.contrib.auth.models import UserManager
from .models import Banks, Countries, Currencies, Parties, customer
from django.shortcuts import get_object_or_404
from rest_framework import serializers


User = get_user_model()


class BankSignupSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.CharField()
    phone = serializers.CharField()
    password = serializers.CharField() 
    address_line_1 = serializers.CharField()
    address_line_2 = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()
    zipcode = serializers.CharField()
    country_code = serializers.PrimaryKeyRelatedField(queryset = Countries.objects.all())

    def create(self, validated_data):
        name = validated_data.pop("name")
        email = validated_data.pop("email")
        phone = validated_data.pop("phone")
        password = validated_data.pop("password")
        country_code = validated_data.pop("country_code")
        address_line_1 = validated_data.pop("address_line_1")
        address_line_2 = validated_data.pop('address_line_2')
        city = validated_data.pop('city')
        zipcode = validated_data.pop('zipcode')
        user = User.objects.create(**validated_data, email = email,username = phone, user_type = 1 , is_staff = True)
        user.set_password(password)
        user.save()
        Banks.objects.create(user = user , name = name , address_line_1 = address_line_1 , address_line_2 = address_line_2 , city = city , zipcode = zipcode , country_code = country_code)
        return user


class PartiesSignupSerailizer(serializers.Serializer):
    email = serializers.CharField()
    phone = serializers.CharField()
    password = serializers.CharField() 
    name = serializers.CharField()
    customer_id = serializers.CharField()
    country_code = serializers.PrimaryKeyRelatedField(queryset = Countries.objects.all())
    account_number = serializers.CharField()
    name = serializers.CharField()
    base_currency = serializers.PrimaryKeyRelatedField(queryset = Currencies.objects.all())
    address_1 = serializers.CharField()
    address_2 = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()
    zipcode = serializers.CharField()

    def create(self, validated_data):
        model_type = validated_data.pop("model_type")
        email = validated_data.pop('email')
        phone = validated_data.pop('phone')
        bank = validated_data.pop("bank")
        name = validated_data.pop('name')
        country_code = validated_data.pop("country_code")
        customer_user_id = validated_data.pop('customer_user_id')
        account_number = validated_data.pop('account_number')
        name = validated_data.pop('name')
        base_currency = validated_data.pop("base_currency")
        address_1 = validated_data.pop("address_1")
        address_2 = validated_data.pop('address_2')
        city = validated_data.pop('city')
        zipcode = validated_data.pop('zipcode')
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data , username = phone,  user_type = 2)
        user.set_password(password)
        user.save()
        Parties.objects.create(
            model_type = model_type , bank_related = bank , user = user ,country_code = country_code ,customers_user_id = customer_user_id , account_number = account_number , name = name ,base_currency = base_currency , address_line_1 = address_1 , address_line_2 = address_2 , city = city , zipcode =zipcode
        )
        return user


class CustomerSignupSerializer(serializers.Serializer):
    email = serializers.CharField()
    phone = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    display_name = serializers.CharField()
    # user_group_belongs = serializers.PrimaryKeyRelatedField(queryset = user_group.objects.all())
    party_type = serializers.PrimaryKeyRelatedField(queryset = Parties.objects.all())
    password = serializers.CharField() 
    
    def create(self, validated_data):
        email = validated_data.pop('email')
        phone = validated_data.pop('phone')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        display_name = validated_data.pop('display_name')
        user_group_belongs = validated_data.pop('user_group_belongs')
        party_type = validated_data.pop('party_type')
        password = validated_data.pop("password")
        user = User.objects.create(username = phone , email = email ,  user_type = 3)
        user.set_password(password)
        user.save()
        customer.objects.create(
            first_name = first_name , last_name = last_name , display_name = display_name , user = user , email = email , phone = phone ,  user_group_type_id = user_group_belongs , party_type_id = party_type
        )
        return user


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone", "password"]

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = customer
        fields = '__all__'

class GetUserSerilaizer(serializers.ModelSerializer):
    customers = CustomerSerializer(read_only=True)
    

    class Meta:
        model = User
        fields = [
            "id",
            "password",
            "last_login",
            "is_admin",
            "username",
            "email",
            "created_date",
            "customers",
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
    customers = CustomerSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "is_active", "customers"]


class CurrenciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currencies
        fields = '__all__'

class Countriesserializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        fields = '__all__'




