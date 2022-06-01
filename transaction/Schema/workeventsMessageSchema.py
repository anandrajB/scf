from graphene_django import DjangoObjectType
from transaction.models import Invoiceuploads, Programs, workevents, Invoices, workflowitems
import graphene
import json
from transaction.Schema.workitemeventsSchema import workeventsType
from accounts.models import Parties


class WorkeventsmessageType(DjangoObjectType):

    class Meta:
        model = workevents
        fields = '__all__'

    status = graphene.String()
    display_name = graphene.String()
    record_datas = graphene.String()
    created_by = graphene.String()

    from_party = graphene.String()
    to_party = graphene.String()

    wf_item_id = graphene.Int()
    invoice = graphene.Int()
    program = graphene.Int()
    invoice_upload = graphene.Int()

    def resolve_program(self, info):
        return self.workitems.program.id

    def resolve_invoice(self, info):
        return self.workitems.invoice.id

    def resolve_invoice_upload(self, info):
        return self.workitems.uploads.id

    def resolve_wf_item_id(self, info):
        return self.workitems.id

    def resolve_from_party(self, info):
        return self.from_party.name

    def resolve_to_party(self, info):
        return self.to_party.name

    def resolve_created_by(self, info):
        return self.workitems.user.email

    def resolve_record_datas(self, info):
        item_id = self.workitems
        if self.type == "PROGRAM":
            qs = Programs.objects.filter(workflowitems=item_id).values()
        elif self.type == "INVOICE":
            qs = Invoices.objects.filter(workflowitems=item_id).values()
        elif self.type == "UPLOAD":
            qs = Invoiceuploads.objects.filter(
                workflowitems=item_id).values()
        return qs

    def resolve_display_name(self, info):
        return self.workitems.user.display_name

    def resolve_status(self, info):
        return self.to_state