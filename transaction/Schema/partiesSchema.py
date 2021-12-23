import graphene
from graphene_django import DjangoObjectType
from accounts.models import Banks, Countries, Currencies, Parties, User


class PartiesType(DjangoObjectType):
    class Meta:
        model = Parties
        fields = '__all__'


class PartiesType_create(graphene.Mutation):
    class Arguments:
        model_id = graphene.Int()
        customers_user_id = graphene.String(required=True)
        account_number = graphene.String(required=True)
        name = graphene.String(required=True)
        bank_related = graphene.Int()
        email = graphene.String()
        phone = graphene.String()
        password = graphene.String()
        base_currency = graphene.Int()
        address_line_1 = graphene.String(required=True)
        address_line_2 = graphene.String(required=True)
        city = graphene.String(required=True)
        state = graphene.String(required=True)
        zipcode = graphene.String(required=True)
        country_code = graphene.Int()
        customer = graphene.Boolean(required=True)

    parties = graphene.Field(PartiesType)

    def mutate(self, root, model_id, email, phone, password, customers_user_id, bank_related, account_number, name, base_currency, address_line_1, address_line_2, city, state, zipcode, country_code, customer):

        _bank = Banks.objects.get(id=bank_related)
        _currency = Currencies.objects.get(id=base_currency)
        _country = Countries.objects.get(id=country_code)
        _user = User.objects.create(
            email=email, phone=phone, username=phone, user_type=2)
        _user.set_password(password)
        _user.save()

        _party = Parties.objects.create( customers_user_id=customers_user_id, account_number=account_number, name=name, base_currency=_currency, bank_related=_bank, user=_user,
                                        address_line_1=address_line_1, address_line_2=address_line_2, city=city, state=state, zipcode=zipcode, country_code=_country, customer=customer)

        return PartiesType_create(parties=_party)


class PartiesType_update(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        model_id = graphene.Int()
        customers_user_id = graphene.String()
        account_number = graphene.String()
        name = graphene.String()
        base_currency = graphene.Int()
        bank_related = graphene.Int()
        address_line_1 = graphene.String()
        address_line_2 = graphene.String()
        city = graphene.String()
        state = graphene.String()
        zipcode = graphene.String()
        country_code = graphene.Int()
        customer = graphene.Boolean()

    parties = graphene.Field(PartiesType)

    def mutate(self, root, id, model_id, customers_user_id, bank_related, user, account_number, name, base_currency, address_line_1, address_line_2, city, state, zipcode, country_code, customer):

        _bank = Banks.objects.get(id=bank_related)
        _currency = Currencies.objects.get(id=base_currency)
        _country = Countries.objects.get(id=country_code)
        

        _party = Parties.objects.get(id=id)
        _party.customers_user_id = customers_user_id
        _party.account_number = account_number
        _party.name = name
        # _party.user = _user
        _party.bank_related = _bank
        _party.base_currency = _currency
        _party.address_line_1 = address_line_1
        _party.address_line_2 = address_line_2
        _party.city = city
        _party.state = state
        _party.zipcode = zipcode
        _party.country_code = _country
        _party.customer = customer
        _party.save()
        return PartiesType_update(parties=_party)


class PartiesType_delete(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    parties = graphene.Field(PartiesType)

    def mutate(self, root, id):
        _party = Parties.objects.get(id=id)
        _party.delete()
        return PartiesType_delete(parties=_party)
