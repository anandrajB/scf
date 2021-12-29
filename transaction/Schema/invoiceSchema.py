# Altered Invoices
import graphene
from graphene_django import DjangoObjectType
from transaction.models import Pairings, Invoices
from accounts.models import Currencies, workflowitems
# from accounts.models import Parties, User, customer, Currencies, Countries, user_group
from transaction.Schema.choices import financeType


class InvoiceType(DjangoObjectType):
    class Meta:
        model = Invoices
        fields = '__all__'


class createInvoice(graphene.Mutation):
    class Arguments:
        pairing = graphene.Int()
        invoice_no = graphene.String()
        # currency = graphene.Int()
        invoice_currency_id = graphene.Int()
        amount = graphene.Int()
        finance_req_type = graphene.Argument(financeType
                                             )
        finance_currency_type_id = graphene.Int()
        settlement_currency_type_id = graphene.Int()
        interest_rate = graphene.Int()
        financed_amount = graphene.Int()
        bank_load_id = graphene.String()
        wf_item_id = graphene.Int()

    invoice = graphene.Field(InvoiceType)

    def mutate(self, root, pairing, invoice_no, invoice_currency_id, amount, finance_req_type, finance_currency_type_id, settlement_currency_type_id, interest_rate, financed_amount, bank_load_id, wf_item_id):

        pairing = Pairings.objects.get(id=pairing)
        invoice_currency = Currencies.objects.get(id=invoice_currency_id)
        finance_currency_type = Currencies.objects.get(
            id=finance_currency_type_id)
        settlement_currency_type = Currencies.objects.get(
            id=settlement_currency_type_id)
        wf_item = workflowitems.objects.get(id=wf_item_id)

        _invoice = Invoices.objects.create(
            pairing=pairing, invoice_no=invoice_no, invoice_currency=invoice_currency, amount=amount, finance_req_type=finance_req_type, finance_currency_type=finance_currency_type, settlement_currency_type=settlement_currency_type, interest_rate=interest_rate, financed_amount=financed_amount, bank_load_id=bank_load_id, wf_item=wf_item)
        return createInvoice(invoice=_invoice)


class updateInvoice(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        pairing = graphene.Int()
        invoice_no = graphene.String()
        invoice_currency_id = graphene.Int()
        amount = graphene.Int()
        finance_req_type = graphene.Argument(financeType
                                             )
        finance_currency_type_id = graphene.Int()
        settlement_currency_type_id = graphene.Int()
        interest_rate = graphene.Int()
        financed_amount = graphene.Int()
        bank_load_id = graphene.String()
        wf_item_id = graphene.Int()

    invoice = graphene.Field(InvoiceType)

    def mutate(self, root, pairing, invoice_no, invoice_currency_id, amount, finance_req_type, finance_currency_type_id, settlement_currency_type_id, interest_rate, financed_amount, bank_load_id, wf_item_id):
        pairing = Pairings.objects.get(id=pairing)
        invoice_currency = Currencies.objects.get(id=invoice_currency_id)
        finance_currency_type = Currencies.objects.get(
            id=finance_currency_type_id)
        settlement_currency_type = Currencies.objects.get(
            id=settlement_currency_type_id)
        wf_item = workflowitems.objects.get(id=wf_item_id)

        _invoice = Invoices.objects.get(id=id)
        _invoice.pairing = pairing
        _invoice.invoice_no = invoice_no
        _invoice.invoice_currency = invoice_currency
        _invoice.amount = amount
        _invoice.finance_req_type = finance_req_type
        _invoice.finance_currency_type = finance_currency_type
        _invoice.settlement_currency_type = settlement_currency_type
        _invoice.interest_rate = interest_rate
        _invoice.financed_amount = financed_amount
        _invoice.bank_load_id = bank_load_id
        _invoice.wf_item = wf_item
        _invoice.save()
        return updateInvoice(invoice=_invoice)


class deleteInvoice(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    invoice = graphene.Field(InvoiceType)

    def mutate(self, root, id):
        _invoice = Invoices.objects.get(id=id)
        _invoice.delete()
        return deleteInvoice(invoice=_invoice)
