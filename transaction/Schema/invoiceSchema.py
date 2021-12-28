import graphene
from graphene_django import DjangoObjectType
from transaction.models import Pairings, Invoices, FundingRequest
# from accounts.models import Parties, User, customer, Currencies, Countries, user_group
from transaction.Schema.programsSchema import financeType


class InvoiceType(DjangoObjectType):
    class Meta:
        model = Invoices
        fields = '__all__'


class createInvoice(graphene.Mutation):
    class Arguments:
        pairing = graphene.Int()
        invoice_no = graphene.String()
        currency = graphene.String()
        amount = graphene.Int()
        finance_type = graphene.Argument(financeType
                                         )
        funding_req_id = graphene.Int()

    invoice = graphene.Field(InvoiceType)

    def mutate(self, root, pairing, invoice_no, currency, amount, finance_type, funding_req_id):
        pairing = Pairings.objects.get(id=pairing)
        funding = FundingRequest.objects.get(id=funding_req_id)

        _invoice = Invoices.objects.create(pairing=pairing, invoice_no=invoice_no, currency=currency,
                                           amount=amount, finance_type=finance_type, funding_req_id=funding)
        return createInvoice(invoice=_invoice)


class updateInvoice(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        pairing = graphene.Int()
        invoice_no = graphene.String()
        currency = graphene.String()
        amount = graphene.Int()
        finance_type = graphene.Argument(financeType)
        funding_req_id = graphene.Int()

    invoice = graphene.Field(InvoiceType)

    def mutate(self, root, id,  pairing, invoice_no, currency, amount, finance_type, funding_req_id):
        pairing = Pairings.objects.get(id=pairing)
        funding = FundingRequest.objects.get(id=funding_req_id)

        _invoice = Invoices.objects.get(id=id)
        _invoice.pairing = pairing
        _invoice.invoice_no = invoice_no
        _invoice.currency = currency
        _invoice.amount = amount
        _invoice.finance_type = finance_type
        _invoice.funding_req_id = funding
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
