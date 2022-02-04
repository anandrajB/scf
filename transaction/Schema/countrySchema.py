import graphene
from graphene_django import DjangoObjectType
from accounts.models import Countries


class CountryType(DjangoObjectType):
    class Meta:
        model = Countries
        fields = '__all__'


class createCountry(graphene.Mutation):
    class Arguments:
        country_name = graphene.String()

    country = graphene.Field(CountryType)

    def mutate(self, root, country_name):
        _country = Countries.objects.create(country_name=country_name)
        return createCountry(country=_country)


class updateCountry(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        country_name = graphene.String()

    country = graphene.Field(CountryType)

    def mutate(self, root, id, country_name):
        _country = Countries.objects.get(id=id)
        _country.country_name = country_name
        _country.save()
        return updateCountry(country=_country)


class deleteCountry(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    country = graphene.Field(CountryType)

    def mutate(self, root, id):
        _country = Countries.objects.get(id=id)
        _country.delete()
        return deleteCountry(country=_country)
