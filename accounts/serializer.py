from django.contrib.auth import get_user_model
from django.contrib.auth.models import UserManager

from transaction.models import Programs

from .models import Banks, Countries, Currencies, Parties, customer , workevents , workflowitems
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
        state = validated_data.pop('state')
        zipcode = validated_data.pop('zipcode')
        user = User.objects.create(**validated_data, email = email,username = phone, user_type = 1 , is_staff = True)
        user.set_password(password)
        user.save()
        Banks.objects.create(user = user , name = name , address_line_1 = address_line_1 , address_line_2 = address_line_2 , city = city ,state = state, zipcode = zipcode , country_code = country_code)
        return user


class PartiesSignupSerailizer(serializers.Serializer):
    party_type_choices = [
    ('CUSTOMER','CUSTOMER'),
    ('BANK','BANK'),
    ('OTHER','OTHER')
    ]

    email = serializers.CharField()
    phone = serializers.CharField()
    password = serializers.CharField() 
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
        email = validated_data.pop('email')
        phone = validated_data.pop('phone')
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
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data , username = phone, email = email ,  user_type = 2)
        user.set_password(password)
        user.save()
        Parties.objects.create(
            party_type = party_type , user = user ,onboarded = on_boarded,state = state,country_code = country_code ,customer_id = customer_user_id , name = name ,base_currency = base_currency , address_line_1 = address_1 , address_line_2 = address_2 , city = city , zipcode =zipcode
        )
        return user


class CustomerSignupSerializer(serializers.Serializer):
    email = serializers.CharField()
    phone = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    display_name = serializers.CharField()
    party = serializers.PrimaryKeyRelatedField(queryset = Parties.objects.all())
    password = serializers.CharField() 
    supervisor = serializers.BooleanField()
    administrator = serializers.BooleanField()
    
    def create(self, validated_data):
        email = validated_data.pop('email')
        phone = validated_data.pop('phone')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        display_name = validated_data.pop('display_name')
        party = validated_data.pop('party')
        password = validated_data.pop("password")
        supervisor = validated_data.pop('supervisor')
        administrator = validated_data.pop('administrator')
        user = User.objects.create(username = phone , email = email ,  user_type = 3)
        user.set_password(password)
        user.save()
        customer.objects.create(
            first_name = first_name , party = party, is_administrator = administrator, is_supervisor = supervisor , last_name = last_name , display_name = display_name , user = user , email = email , phone = phone  )
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






# class Workeventsserializer(serializers.ModelSerializer):
#     class Meta:
#         model = workevents
#         fields = '__all__'


# class Workitemserializer(serializers.ModelSerializer):
#     workevent  = Workeventsserializer(many= True,read_only = True)
#     class Meta:
#         model = workflowitems
#         fields = [
#             'created_date',
#             'workevent'
#         ]
#         read_only_fields = ['workevent']



