# Altered Pairings

import graphene
from graphene_django import DjangoObjectType
from transaction.models import Programs, Pairings
from accounts.models import Currencies, Parties
from transaction.Schema.choices import financeType, interestType, interestRate


class PairingType(DjangoObjectType):
    class Meta:
        model = Pairings
        fields = '__all__'


class createPairing(graphene.Mutation):
    class Arguments:
        program_type_id = graphene.Int()
        counterparty_id = graphene.Int()
        finance_request = graphene.Argument(financeType)
        currency = graphene.String()
        total_limit = graphene.Int()
        finance_currency_type_id = graphene.Int()
        settlement_currency_type_id = graphene.Int()
        expiry_date = graphene.Date()
        max_finance_percentage = graphene.Int()
        max_invoice_age_for_funding = graphene.Int()
        max_age_for_repayment = graphene.Int()
        minimum_period = graphene.Int()
        maximum_period = graphene.Int()
        minimum_amount_currency = graphene.String()
        minimum_amount = graphene.Int()
        maximum_amount = graphene.Int()
        financed_amount = graphene.Int()
        balance_amount = graphene.Int()
        grace_period = graphene.Int()
        interest_type = graphene.Argument(interestType)
        interest_rate_type = graphene.Argument(interestRate)
        interest_rate = graphene.Int()
        margin = graphene.Int()

    pairing = graphene.Field(PairingType)

    def mutate(self, root, program_type_id, counterparty_id, finance_request, currency, total_limit, finance_currency_type_id, settlement_currency_type_id, expiry_date, max_finance_percentage, max_invoice_age_for_funding,
               max_age_for_repayment, minimum_period, maximum_period, minimum_amount_currency, minimum_amount, maximum_amount, financed_amount, balance_amount, grace_period, interest_type, interest_rate_type, interest_rate, margin):

        program = Programs.objects.get(id=program_type_id)
        counterparty = Parties.objects.get(id=counterparty_id)
        finance_currency_type = Currencies.objects.get(
            id=finance_currency_type_id)
        settlement_currency_type = Currencies.objects.get(
            id=settlement_currency_type_id)

        _pairing = Pairings.objects.create(
            program_type=program, counterparty=counterparty, finance_request=finance_request, currency=currency, total_limit=total_limit, expiry_date=expiry_date,
            finance_currency_type=finance_currency_type, settlement_currency_type=settlement_currency_type, max_finance_percentage=max_finance_percentage, max_invoice_age_for_funding=max_invoice_age_for_funding, max_age_for_repayment=max_age_for_repayment,
            minimum_period=minimum_period, maximum_period=maximum_period, minimum_amount_currency=minimum_amount_currency, minimum_amount=minimum_amount, maximum_amount=maximum_amount, financed_amount=financed_amount, balance_amount=balance_amount, grace_period=grace_period, interest_type=interest_type,
            interest_rate_type=interest_rate_type, interest_rate=interest_rate, margin=margin)
        return createPairing(pairing=_pairing)


class updatePairing(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        program_type_id = graphene.Int()
        counterparty_id = graphene.Int()
        finance_request = graphene.Argument(financeType)
        currency = graphene.String()
        total_limit = graphene.Int()
        finance_currency_type_id = graphene.Int()
        settlement_currency_type_id = graphene.Int()
        expiry_date = graphene.Date()
        max_finance_percentage = graphene.Int()
        max_invoice_age_for_funding = graphene.Int()
        max_age_for_repayment = graphene.Int()
        minimum_period = graphene.Int()
        maximum_period = graphene.Int()
        minimum_amount_currency = graphene.String()
        minimum_amount = graphene.Int()
        maximum_amount = graphene.Int()
        financed_amount = graphene.Int()
        balance_amount = graphene.Int()
        grace_period = graphene.Int()
        interest_type = graphene.Argument(interestType)
        interest_rate_type = graphene.Argument(interestRate)
        interest_rate = graphene.Int()
        margin = graphene.Int()

    pairing = graphene.Field(PairingType)

    def mutate(self, root, program_type_id, counterparty_id, finance_request, currency, total_limit, finance_currency_type_id, settlement_currency_type_id, expiry_date, max_finance_percentage, max_invoice_age_for_funding,
               max_age_for_repayment, minimum_period, maximum_period, minimum_amount_currency, minimum_amount, maximum_amount, financed_amount, balance_amount, grace_period, interest_type, interest_rate_type, interest_rate, margin):

        program = Programs.objects.get(id=program_type_id)
        counterparty = Parties.objects.get(id=counterparty_id)
        finance_currency_type = Currencies.objects.get(
            id=finance_currency_type_id)
        settlement_currency_type = Currencies.objects.get(
            id=settlement_currency_type_id)

        _pairing = Pairings.objects.get(id=id)
        _pairing.program_type = program
        _pairing.counterparty = counterparty
        _pairing.finance_request = finance_request
        _pairing.currency = currency
        _pairing.total_limit = total_limit
        _pairing.expiry_date = expiry_date
        _pairing.finance_currency_type = finance_currency_type
        _pairing.settlement_currency_type = settlement_currency_type
        _pairing.max_finance_percentage = max_finance_percentage
        _pairing.max_invoice_age_for_funding = max_invoice_age_for_funding
        _pairing.max_age_for_repayment = max_age_for_repayment
        _pairing.minimum_period = minimum_period
        _pairing.maximum_period = maximum_period
        _pairing.minimum_amount_currency = minimum_amount_currency
        _pairing.minimum_amount = minimum_amount
        _pairing.maximum_amount = maximum_amount
        _pairing.financed_amount = financed_amount
        _pairing.balance_amount = balance_amount
        _pairing.grace_period = grace_period
        _pairing.interest_type = interest_type
        _pairing.interest_rate_type = interest_rate_type
        _pairing.interest_rate = interest_rate
        _pairing.margin = margin

        _pairing.save()
        return updatePairing(pairing=_pairing)


class deletePairing(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    pairing = graphene.Field(PairingType)

    def mutate(self, root, id):
        _pairing = Pairings.objects.get(id=id)
        _pairing.delete()
        return deletePairing(pairing=_pairing)
