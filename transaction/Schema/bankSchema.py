# import graphene
# from graphene_django import DjangoObjectType
# from accounts.models import Banks, Countries, Currencies, User


# class BankType(DjangoObjectType):
#     class Meta:
#         model = Banks
#         fields = '__all__'


# class createBank(graphene.Mutation):
#     class Arguments:
#         name = graphene.String()
#         email = graphene.String()
#         phone = graphene.String()
#         password = graphene.String()
#         base_currency = graphene.Int()
#         address_line = graphene.String()
#         address_line_2 = graphene.String()
#         city = graphene.String()
#         state = graphene.String()
#         zipcode = graphene.String()
#         country_code = graphene.Int()

#     bank = graphene.Field(BankType)

#     def mutate(self, root, name, email, phone, password, base_currency, address_line, address_line_2, city, state, zipcode, country_code):
#         _country = Countries.objects.get(id=country_code)
#         _currency = Currencies.objects.get(id=base_currency)

#         _user = User.objects.create(
#             username=phone, email=email, user_type=1, is_staff=True, phone=phone)
#         _user.set_password(password)
#         _user.save()

#         _bank = Banks.objects.create(name=name, user=_user, base_currency=_currency, address_line=address_line,
#                                      address_line_2=address_line_2, city=city, state=state, zipcode=zipcode, country_code=_country)
#         return createBank(bank=_bank)
