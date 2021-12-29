import graphene
from graphene_django import DjangoObjectType
from accounts.models import workflowitems


class workflowitemType(DjangoObjectType):
    class Meta:
        model = workflowitems
        fields = '__all__'
