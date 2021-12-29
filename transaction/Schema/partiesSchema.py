# Altered Parties
import graphene
from graphene_django import DjangoObjectType
from accounts.models import Banks, Countries, Currencies, Parties, User


class PartiesType(DjangoObjectType):
    class Meta:
        model = Parties
        fields = '__all__'


# class PartiesType_create(graphene.Mutation):
#     class Arguments:
#         customers_id = graphene.String(required=True)
#         name = graphene.String(required=True)
#         email = graphene.String()
#         phone = graphene.String()
#         password = graphene.String()
#         base_currency = graphene.Int()
#         address_line_1 = graphene.String(required=True)
#         address_line_2 = graphene.String(required=True)
#         city = graphene.String(required=True)
#         state = graphene.String(required=True)
#         zipcode = graphene.String(required=True)
#         country_code = graphene.Int()
#         onboarded = graphene.Boolean()
#         party_type_id = graphene.Int()

#     parties = graphene.Field(PartiesType)

#     def mutate(self, root, email, phone, password, customer_id, name, base_currency, address_line_1, address_line_2, city, state, zipcode, country_code, onboarded, party_type_id):
#         party_type = Partytype.objects.get(id=party_type_id)
#         _currency = Currencies.objects.get(id=base_currency)
#         _country = Countries.objects.get(id=country_code)
#         _user = User.objects.create(
#             email=email, phone=phone, username=phone, user_type=2)
#         _user.set_password(password)
#         _user.save()

#         _party = Parties.objects.create(customer_id=customer_id, name=name, base_currency=_currency, user=_user,
#                                         address_line_1=address_line_1, address_line_2=address_line_2, city=city, state=state, zipcode=zipcode, country_code=_country, onboarded=onboarded,
#                                         party_type=party_type)

#         return PartiesType_create(parties=_party)


# class PartiesType_update(graphene.Mutation):
#     class Arguments:
#         id = graphene.ID()
#         customers_id = graphene.String(required=True)
#         name = graphene.String(required=True)
#         email = graphene.String()
#         phone = graphene.String()
#         password = graphene.String()
#         base_currency = graphene.Int()
#         address_line_1 = graphene.String(required=True)
#         address_line_2 = graphene.String(required=True)
#         city = graphene.String(required=True)
#         state = graphene.String(required=True)
#         zipcode = graphene.String(required=True)
#         country_code = graphene.Int()
#         onboarded = graphene.Boolean()
#         party_type_id = graphene.Int()

#     parties = graphene.Field(PartiesType)

#     def mutate(self, root, customer_id, name, base_currency, address_line_1, address_line_2, city, state, zipcode, country_code, onboarded, party_type_id):
#         party_type = Partytype.objects.get(id=party_type_id)
#         _currency = Currencies.objects.get(id=base_currency)
#         _country = Countries.objects.get(id=country_code)

#         _party = Parties.objects.get(id=id)
#         _party.customer_id = customer_id
#         _party.name = name
#         _party.base_currency = _currency
#         _party.address_line_1 = address_line_1
#         _party.address_line_2 = address_line_2
#         _party.city = city
#         _party.state = state
#         _party.zipcode = zipcode
#         _party.country_code = _country
#         _party.onboarded = onboarded
#         _party.party_type = party_type
#         _party.save()
#         return PartiesType_update(parties=_party)


# class PartiesType_delete(graphene.Mutation):
#     class Arguments:
#         id = graphene.ID()

#     parties = graphene.Field(PartiesType)

#     def mutate(self, root, id):
#         _party = Parties.objects.get(id=id)
#         _party.delete()
#         return PartiesType_delete(parties=_party)
