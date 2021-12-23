import graphene
from graphene_django import DjangoObjectType
from transaction.models import  ProgramType, Programs
from accounts.models import Parties
from transaction.Schema.choices import financeType, interestRate, interestType


class ProgramsType(DjangoObjectType):
    class Meta:
        model = Programs
        fields = '__all__'


class createPrograms(graphene.Mutation):
    class Arguments:
        model_id = graphene.Int()
        party_id = graphene.Int()
        programtype_id = graphene.Int()
        finance_type = graphene.Argument(financeType)
        currency = graphene.String(required=True)
        max_total_limit = graphene.Int(required=True)
        expiry = graphene.Date(required=True)
        max_finance_percentage = graphene.Int(required=True)
        max_age_for_repayment = graphene.Int()
        minimum_period = graphene.Int()
        maximum_period = graphene.Int()
        minimum_amount_currency = graphene.String(required=True)
        minimum_amount = graphene.Int(required=True)
        financed_amount = graphene.Int(required=True)
        balance_amount = graphene.Int(required=True)
        grace_period = graphene.Int()
        interest_type = graphene.Argument(interestType)
        interest_rate = graphene.Argument(interestRate)
        margin = graphene.Int(required=True)

    _programs = graphene.Field(ProgramsType)

    def mutate(self, root, model_id, party_id, programtype_id, finance_type, currency, max_total_limit, expiry, max_finance_percentage, max_age_for_repayment, minimum_period, maximum_period,
               minimum_amount_currency, minimum_amount, financed_amount, balance_amount, grace_period, interest_type, interest_rate, margin):
        party = Parties.objects.get(id=party_id)
        programtype = ProgramType.objects.get(id=programtype_id)

        if not party and not programtype:
            raise Exception("Invalid Details")

        _program = Programs.objects.create( party=party, program_model=programtype, finance_type=finance_type, currency=currency, max_total_limit=max_total_limit, expiry=expiry, max_finance_percentage=max_finance_percentage, max_age_for_repayment=max_age_for_repayment,
                                           minimum_period=minimum_period, maximum_period=maximum_period, minimum_amount_currency=minimum_amount_currency, minimum_amount=minimum_amount, financed_amount=financed_amount, balance_amount=balance_amount, grace_period=grace_period, interest_type=interest_type, interest_rate=interest_rate, margin=margin)
        return createPrograms(_programs=_program)


class updatePrograms(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        model_id = graphene.Int()
        party_id = graphene.Int()
        programtype_id = graphene.Int()
        finance_type = graphene.Argument(financeType)
        currency = graphene.String(required=True)
        max_total_limit = graphene.Int(required=True)
        expiry = graphene.Date(required=True)
        max_finance_percentage = graphene.Int(required=True)
        max_age_for_repayment = graphene.Int()
        minimum_period = graphene.Int()
        maximum_period = graphene.Int()
        minimum_amount_currency = graphene.String(required=True)
        minimum_amount = graphene.Int(required=True)
        financed_amount = graphene.Int(required=True)
        balance_amount = graphene.Int(required=True)
        grace_period = graphene.Int()
        interest_type = graphene.Argument(interestType)
        interest_rate = graphene.Argument(interestRate)
        margin = graphene.Int(required=True)

    _programs = graphene.Field(ProgramsType)

    def mutate(self, root, id, model_id, party_id, programtype_id, finance_type, currency, max_total_limit, expiry, max_finance_percentage, max_age_for_repayment, minimum_period, maximum_period,
               minimum_amount_currency, minimum_amount, financed_amount, balance_amount, grace_period, interest_type, interest_rate, margin):
        party = Parties.objects.get(id=party_id)
        programtype = ProgramType.objects.get(id=programtype_id)

        _program = Programs.objects.get(id=id)
        _program.party = party
        _program.program_model = programtype
        _program.finance_type = finance_type
        _program.currency = currency
        _program.max_total_limit = max_total_limit
        _program.expiry = expiry
        _program.max_finance_percentage = max_finance_percentage
        _program.max_age_for_repayment = max_age_for_repayment
        _program.minimum_period = minimum_period
        _program.maximum_period = maximum_period
        _program.minimum_amount_currency = minimum_amount_currency
        _program.minimum_amount = minimum_amount
        _program.financed_amount = financed_amount
        _program.balance_amount = balance_amount
        _program.grace_period = grace_period
        _program.interest_type = interest_type
        _program.interest_rate = interest_rate
        _program.margin = margin

        _program.save()
        return updatePrograms(_programs=_program)


class deletePrograms(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    _programs = graphene.Field(ProgramsType)

    def mutate(self, root, id):
        _program = Programs.objects.get(id=id)
        _program.delete()
        return deletePrograms(_programs=_program)
