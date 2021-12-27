# Altered Schema
import graphene
from graphene_django import DjangoObjectType

from transaction.models import invoice_uploads
from accounts.models import workflowitems
from transaction.Schema.choices import ProgramTypeChoices


class InvoiceUploadType(DjangoObjectType):
    class Meta:
        model = invoice_uploads
        field = '__all__'


class create_invoiceUploads(graphene.Mutation):
    class Arguments:
        program_type = graphene.Argument(ProgramTypeChoices)
        invoices = graphene.JSONString()
        wf_item_id = graphene.Int()

    invoiceuploads = graphene.Field(InvoiceUploadType)

    def mutate(self, root, program_type, invoices, wf_item_id):
        wf_item = workflowitems.objects.get(id=wf_item_id)

        _invoiceuploads = invoice_uploads.objects.create(
            program_type=program_type, invoices=invoices, wf_item=wf_item)
        return create_invoiceUploads(invoiceuploads=_invoiceuploads)


class update_invoiceuploads(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        program_type = graphene.Argument(ProgramTypeChoices)
        invoices = graphene.JSONString()
        wf_item_id = graphene.Int()

    invoiceuploads = graphene.Field(InvoiceUploadType)

    def mutate(self, root, id, program_type, invoices, wf_item_id):
        wf_item = workflowitems.objects.get(id=wf_item_id)

        _invoiceuploads = invoice_uploads.objects.get(id=id)
        _invoiceuploads.program_type = program_type
        _invoiceuploads.invoices = invoices
        _invoiceuploads.wf_item = wf_item
        _invoiceuploads.save()
        return update_invoiceuploads(invoiceuploads=_invoiceuploads)


class delete_invoiceuploads(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    invoiceuploads = graphene.Field(InvoiceUploadType)

    def mutate(self, root, id):
        _invoiceuploads = invoice_uploads.objects.get(id=id)
        _invoiceuploads.delete()
        return update_invoiceuploads(invoiceuploads=_invoiceuploads)
