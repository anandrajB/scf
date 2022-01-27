from django.contrib.auth import get_user_model
from transaction.models import Actions, Programs, submodels, workevents
from .models import Banks, Countries, Currencies, Parties, signatures, userprocessauth  
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework import generics


User = get_user_model()

# SERIALIZER'S 

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


    def validate_name(self,value):
        if Parties.objects.filter(name = value).exists():
            raise serializers.ValidationError("A party with this name already exists , try another name")
        return value
        

    


class UserSignupSerializer(serializers.Serializer):
    email = serializers.CharField()
    phone = serializers.CharField()
    party = serializers.PrimaryKeyRelatedField(queryset = Parties.objects.all())
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    display_name = serializers.CharField()
    supervisor = serializers.BooleanField()
    administrator = serializers.BooleanField()
    
    def create(self, validated_data):
        email = validated_data.pop('email')
        phone = validated_data.pop('phone')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        display_name = validated_data.pop('display_name')
        party = validated_data.pop('party')
        supervisor = validated_data.pop('supervisor')
        administrator = validated_data.pop('administrator')
        user = User.objects.create(phone = phone , email = email ,first_name = first_name ,  last_name =last_name ,display_name = display_name , party = party, is_supervisor = supervisor , is_administrator = administrator )
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
            "created_date",
            "is_supervisor",
            "is_administrator",
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



class signaturesserializer(serializers.ModelSerializer):
    party_belongs = serializers.SlugRelatedField(read_only = True , slug_field='name')

    class Meta:
        model = signatures
        fields = [
            'id',
            'party_belongs',
            'sign_a',
            'sign_b',
            'sign_c',
            'workflowitem',
            'action',
        ]


class userprocesserializer(serializers.ModelSerializer):
    class Meta:
        model = userprocessauth
        fields = '__all__'


class signaturesserializer(serializers.ModelSerializer):
    class Meta:
        model = signatures
        fields = '__all__'

        