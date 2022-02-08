import graphene
from graphene_django import DjangoObjectType
from transaction.models import FundingRequest, Programs


class FundingType(DjangoObjectType):
    class Meta:
        model = FundingRequest
        fields = '__all__'


class createFunding(graphene.Mutation):
    class Arguments:
        program = graphene.Int()
        total_amount = graphene.Int()
        financed_amount = graphene.Int()
        balance_amount = graphene.Int()

    funding = graphene.Field(FundingType)

    def mutate(self, root, program, total_amount, financed_amount, balance_amount):
        program = Programs.objects.get(id=program)

        _funding = FundingRequest.objects.create(
            program=program, total_amount=total_amount, financed_amount=financed_amount, balance_amount=balance_amount)
        return createFunding(funding=_funding)


class updateFunding(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        program = graphene.Int()
        total_amount = graphene.Int()
        financed_amount = graphene.Int()
        balance_amount = graphene.Int()

    funding = graphene.Field(FundingType)

    def mutate(self, root, id, program, total_amount, financed_amount, balance_amount):
        program = Programs.objects.get(id=program)

        _funding = FundingRequest.objects.get(id=id)
        _funding.program = program
        _funding.total_amount = total_amount
        _funding.financed_amount = financed_amount
        _funding.balance_amount = balance_amount
        _funding.save()
        return updateFunding(funding=_funding)


class deleteFunding(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    funding = graphene.Field(FundingType)

    def mutate(self, root, id):
        _funding = FundingRequest.objects.get(id=id)
        _funding.delete()
        return deleteFunding(funding=_funding)
