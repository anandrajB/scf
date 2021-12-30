# Altered Programs

import graphene
from graphene_django import DjangoObjectType
from transaction.models import Programs
from accounts.models import Parties, workflowitems
from transaction.Schema.choices import financeType, interestRate, interestType, ProgramTypeChoices
from transaction.Schema import workflowitemSchema


class ProgramsType(DjangoObjectType):
    workflowitems = workflowitemSchema.workflowitemType()

    class Meta:
        model = Programs
        # fields = '__all__'
        fields = [
            'party',
            'program_type',
            'finance_request_type',
            'limit_currency',
            'total_limit_amount',
            'finance_currency',
            'settlement_currency',
            'expiry_date',
            'max_finance_percentage',
            'max_invoice_age_for_funding',
            'max_age_for_repayment',
            'minimum_period',
            'maximum_period',
            'maximum_amount',
            'minimum_amount',
            'financed_amount',
            'balance_amount',
            'grace_period',
            'interest_type',
            'interest_rate_type',
            'interest_rate',
            'margin',
            'workflowitems'
        ]


class createPrograms(graphene.Mutation):
    class Arguments:
        party_id = graphene.Int()
        program_type = graphene.Argument(ProgramTypeChoices)
        finance_request_type = graphene.Argument(financeType)
        limit_currency = graphene.String(required=True)
        total_limit_amount = graphene.Int(required=True)
        finance_currency = graphene.String(required=True)
        settlement_currency = graphene.String(required=True)
        # expiry = graphene.Date(required=True)
        max_finance_percentage = graphene.Int(required=True)
        max_invoice_age_for_funding = graphene.Int()
        max_age_for_repayment = graphene.Int()
        minimum_period = graphene.Int()
        maximum_period = graphene.Int(required=True)
        maximum_amount = graphene.String(required=True)
        minimum_amount = graphene.Int(required=True)
        financed_amount = graphene.Int()
        balance_amount = graphene.Int(required=True)
        grace_period = graphene.Int()
        interest_type = graphene.Argument(interestType)
        interest_rate_type = graphene.Argument(interestRate)
        interest_rate = graphene.Int()
        margin = graphene.Int(required=True)
        wf_item_id = graphene.Int()

    _programs = graphene.Field(ProgramsType)

    def mutate(self, root, party_id, program_type, finance_request_type, limit_currency, total_limit_amount, finance_currency, settlement_currency, max_finance_percentage, max_invoice_age_for_funding, max_age_for_repayment, minimum_period, maximum_period,
               maximum_amount, minimum_amount, financed_amount, balance_amount, grace_period, interest_type, interest_rate_type, interest_rate, margin, wf_item_id):
        party = Parties.objects.get(id=party_id)
        wf_item = workflowitems.objects.get(id=wf_item_id)

        _program = Programs.objects.create(party=party, program_type=program_type, finance_request_type=finance_request_type, limit_currency=limit_currency, total_limit_amount=total_limit_amount, finance_currency=finance_currency, settlement_currency=settlement_currency, max_finance_percentage=max_finance_percentage, max_invoice_age_for_funding=max_invoice_age_for_funding, max_age_for_repayment=max_age_for_repayment,
                                           minimum_period=minimum_period, maximum_period=maximum_period, maximum_amount=maximum_amount, minimum_amount=minimum_amount, financed_amount=financed_amount, balance_amount=balance_amount, grace_period=grace_period, interest_type=interest_type, interest_rate_type=interest_rate_type, interest_rate=interest_rate, margin=margin, wf_item=wf_item)
        return createPrograms(_programs=_program)


class updatePrograms(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        party_id = graphene.Int()
        program_type = graphene.Argument(ProgramTypeChoices)
        finance_request_type = graphene.Argument(financeType)
        limit_currency = graphene.String(required=True)
        total_limit_amount = graphene.Int(required=True)
        finance_currency = graphene.String(required=True)
        settlement_currency = graphene.String(required=True)
        # expiry = graphene.Date(required=True)
        max_finance_percentage = graphene.Int(required=True)
        max_invoice_age_for_funding = graphene.Int()
        max_age_for_repayment = graphene.Int()
        minimum_period = graphene.Int()
        maximum_period = graphene.Int(required=True)
        maximum_amount = graphene.String(required=True)
        minimum_amount = graphene.Int(required=True)
        financed_amount = graphene.Int()
        balance_amount = graphene.Int(required=True)
        grace_period = graphene.Int()
        interest_type = graphene.Argument(interestType)
        interest_rate_type = graphene.Argument(interestRate)
        interest_rate = graphene.Int()
        margin = graphene.Int(required=True)
        wf_item_id = graphene.Int()

    _programs = graphene.Field(ProgramsType)

    def mutate(self, root, party_id, program_type, finance_request_type, limit_currency, total_limit_amount, finance_currency, settlement_currency, max_finance_percentage, max_invoice_age_for_funding, max_age_for_repayment, minimum_period, maximum_period,
               maximum_amount, minimum_amount, financed_amount, balance_amount, grace_period, interest_type, interest_rate_type, interest_rate, margin, wf_item_id):
        party = Parties.objects.get(id=party_id)
        wf_item = workflowitems.objects.get(id=wf_item_id)

        _program = Programs.objects.get(id=id)
        _program.party = party
        _program.program_type = program_type
        _program.finance_request_type = finance_request_type
        _program.limit_currency = limit_currency
        _program.total_limit_amount = total_limit_amount
        # _program.expiry = expiry
        _program.finance_currency = finance_currency
        _program.settlement_currency = settlement_currency
        _program.max_finance_percentage = max_finance_percentage
        _program.max_invoice_age_for_funding = max_invoice_age_for_funding
        _program.max_age_for_repayment = max_age_for_repayment
        _program.minimum_period = minimum_period
        _program.maximum_period = maximum_period
        _program.maximum_amount = maximum_amount
        _program.minimum_amount = minimum_amount
        _program.financed_amount = financed_amount
        _program.balance_amount = balance_amount
        _program.grace_period = grace_period
        _program.interest_type = interest_type
        _program, interest_rate_type = interest_rate_type
        _program.interest_rate = interest_rate
        _program.margin = margin
        _program.wf_item = wf_item

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
