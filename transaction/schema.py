import graphene
from django.db.models import Q
from graphene import relay
from graphene_django import DjangoListField
from accounts.models import customer
from transaction.models import Invoices, Programs
from .Schema import partiesSchema, programsSchema, customerSchema, currencySchema, countrySchema, pairingsSchema, invoiceSchema, fundingSchema, bankSchema, userSchema, invoiceuploadSchema, workitemeventsSchema


class Query(graphene.ObjectType):

    all_users = DjangoListField(userSchema.UserDetail)
    # all_banks = DjangoListField(bankSchema.BankType)
    all_parties = DjangoListField(partiesSchema.PartiesType)
    all_programs = graphene.Field(
        programsSchema.ProgramsType, id=graphene.Int())
    all_customers = graphene.List(
        customerSchema.CustomerType, search=graphene.ID())
    all_currencies = DjangoListField(currencySchema.CurrencyType)
    all_country = DjangoListField(countrySchema.CountryType)
    all_pairings = DjangoListField(pairingsSchema.PairingType)
    all_funding = DjangoListField(fundingSchema.FundingType)
    all_invoices = graphene.List(
        invoiceSchema.InvoiceType, curr_less=graphene.String(), curr_greater=graphene.String())
    all_invoiceuploads = DjangoListField(invoiceuploadSchema.InvoiceUploadType)
    all_workevents = DjangoListField(workitemeventsSchema.workeventsType)

    def resolve_all_programs(self, info, id=None, **kwargs):
        try:
            return Programs.objects.get(id=id)
        except Exception as E:
            return E

    def resolve_all_customers(self, info, search=None, **kwargs):
        if search:
            filter = (
                Q(party_type_id=search)
            )
            return customer.objects.filter(filter)
        return customer.objects.all()

    def resolve_all_invoices(self, info, curr_less=None, curr_greater=None, **kwargs):

        if curr_less:
            return Invoices.objects.filter(currency__lt=curr_less)

        if curr_greater:
            # filter = (
            #     Q(currency__gt=curr_greater)
            # )
            return Invoices.objects.filter(currency__gt=curr_greater)
        return Invoices.objects.all()


class Mutation(graphene.ObjectType):

    # create_bank = bankSchema.createBank.Field()

    # create_parties = partiesSchema.PartiesType_create.Field()
    # update_parties = partiesSchema.PartiesType_update.Field()
    # delete_parties = partiesSchema.PartiesType_delete.Field()

    create_program = programsSchema.createPrograms.Field()
    update_program = programsSchema.updatePrograms.Field()
    delete_program = programsSchema.deletePrograms.Field()

    create_customer = customerSchema.createCustomer.Field()
    update_customer = customerSchema.updateCustomer.Field()
    delete_customer = customerSchema.deleteCustomer.Field()

    create_currency = currencySchema.createCurrency.Field()
    update_currency = currencySchema.updateCurrency.Field()
    delete_currency = currencySchema.deleteCurrency.Field()

    create_country = countrySchema.createCountry.Field()
    update_country = countrySchema.updateCountry.Field()
    delete_country = countrySchema.deleteCountry.Field()

    create_pairing = pairingsSchema.createPairing.Field()
    update_pairing = pairingsSchema.updatePairing.Field()
    delete_pairing = pairingsSchema.deletePairing.Field()

    create_invoice = invoiceSchema.createInvoice.Field()
    update_invoice = invoiceSchema.updateInvoice.Field()
    delete_invoice = invoiceSchema.deleteInvoice.Field()

    create_funding = fundingSchema.createFunding.Field()
    update_funding = fundingSchema.updateFunding.Field()
    delete_funding = fundingSchema.deleteFunding.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
