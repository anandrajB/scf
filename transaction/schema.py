import graphene
from graphene_django import DjangoListField
# from graphene_django.types import DjangoObjectType
from .Schema import workmodelSchema, partiesSchema, programtypeSchema, programsSchema, customerSchema, currencySchema, countrySchema, pairingsSchema, invoiceSchema, fundingSchema, bankSchema, userSchema


class Query(graphene.ObjectType):

    all_users = DjangoListField(userSchema.UserDetail)
    all_workmodel = DjangoListField(workmodelSchema.workmodelType)
    all_banks = DjangoListField(bankSchema.BankType)
    all_parties = DjangoListField(partiesSchema.PartiesType)
    all_programtypes = DjangoListField(programtypeSchema.Program_Type)
    all_programs = DjangoListField(programsSchema.ProgramsType)
    all_customers = DjangoListField(customerSchema.CustomerType)
    all_currencies = DjangoListField(currencySchema.CurrencyType)
    all_country = DjangoListField(countrySchema.CountryType)
    all_pairings = DjangoListField(pairingsSchema.PairingType)
    all_funding = DjangoListField(fundingSchema.FundingType)
    all_invoices = DjangoListField(invoiceSchema.InvoiceType)


class Mutation(graphene.ObjectType):
    create_workmodel = workmodelSchema.workmodelType_create.Field()
    update_workmodel = workmodelSchema.workmodelType_update.Field()
    delete_workmodel = workmodelSchema.workmodelType_delete.Field()

    create_bank = bankSchema.createBank.Field()

    create_parties = partiesSchema.PartiesType_create.Field()
    update_parties = partiesSchema.PartiesType_update.Field()
    delete_parties = partiesSchema.PartiesType_delete.Field()

    create_programtype = programtypeSchema.createProgramType.Field()
    update_programtype = programtypeSchema.updateProgramType.Field()
    delete_programtype = programtypeSchema.deleteProgramType.Field()

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
