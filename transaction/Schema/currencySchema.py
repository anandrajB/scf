import graphene
from graphene_django import DjangoObjectType
from accounts.models import Currencies

class CurrencyType(DjangoObjectType):
    class Meta:
        model = Currencies
        fields = '__all__'

class createCurrency(graphene.Mutation):
    class Arguments:
        iso = graphene.Int()
        description = graphene.String()

    currency = graphene.Field(CurrencyType)

    def mutate(self, root, iso, description):
        _currency = Currencies.objects.create(iso=iso, description=description)
        return createCurrency(currency=_currency)


class updateCurrency(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        iso = graphene.Int()
        description = graphene.String()

    currency = graphene.Field(CurrencyType)

    def mutate(self, root, id, iso, description):
        _currency = Currencies.objects.get(id=id)
        _currency.iso = iso
        _currency.description = description
        _currency.save()
        return updateCurrency(currency=_currency)


class deleteCurrency(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    currency = graphene.Field(CurrencyType)

    def mutate(self, root, id):
        _currency = Currencies.objects.get(id=id)
        _currency.delete()
        return deleteCurrency(currency=_currency)
