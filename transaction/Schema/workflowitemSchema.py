import graphene
from graphene_django import DjangoObjectType
from accounts.models import workflowitems
from transaction.Schema import workitemeventsSchema


class workflowitemType(DjangoObjectType):
    workflowevent = workitemeventsSchema.workeventsType()

    class Meta:
        model = workflowitems
        fields = [
            'initial_state',
            'current_state',
            'workflowevent'
        ]
