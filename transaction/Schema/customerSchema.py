import graphene
from graphene_django import DjangoObjectType
from accounts.models import Parties, User, customer


class CustomerType(DjangoObjectType):
    class Meta:
        model = customer
        fields = '__all__'


class createCustomer(graphene.Mutation):
    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        display_name = graphene.String()
        email = graphene.String()
        phone = graphene.String()
        password = graphene.String()
        user_group_type_id = graphene.Int()
        party_type_id = graphene.Int()

    customers = graphene.Field(CustomerType)

    def mutate(self, root, first_name, last_name, display_name, email, phone, password, user_group_type_id, party_type_id):
        party = Parties.objects.get(id=party_type_id)

        _user = User.objects.create(
            username=phone, phone=phone, email=email, user_type=3)
        _user.set_password(password)
        _user.save()

        _customer = customer.objects.create(first_name=first_name, last_name=last_name, display_name=display_name,
                                            user=_user, email=email, phone=phone, party_type_id=party)
        return createCustomer(customers=_customer)


class updateCustomer(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        first_name = graphene.String()
        last_name = graphene.String()
        display_name = graphene.String()
        user = graphene.Int()
        email = graphene.String()
        phone = graphene.String()
        user_group_type_id = graphene.Int()
        party_type_id = graphene.Int()

    customers = graphene.Field(CustomerType)

    def mutate(self, root, first_name, last_name, display_name, user, email, phone, user_group_type_id, party_type_id):
        user = User.objects.get(id=user)
        party = Parties.objects.get(id=party_type_id)

        _customer = customer.objects.get(id=id)
        _customer.first_name = first_name
        _customer.last_name = last_name
        _customer.user = user
        _customer.party_type_id = party
        _customer.display_name = display_name
        _customer.email = email
        _customer.phone = phone
        _customer.save()
        return updateCustomer(customers=_customer)


class deleteCustomer(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    customers = graphene.Field(CustomerType)

    def mutate(self, root, id):
        _customer = customer.objects.get(id=id)
        _customer.delete()
        return deleteCustomer(customers=_customer)
