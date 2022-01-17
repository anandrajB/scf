import graphene
from graphene_django import DjangoObjectType
from transaction.models import workevents


class workeventsType(DjangoObjectType):
    class Meta:
        model = workevents
        fields = '__all__'
