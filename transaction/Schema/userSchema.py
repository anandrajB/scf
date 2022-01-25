from graphene_django import DjangoObjectType
from accounts.models import User


class UserDetail(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "phone")
