from transaction.query import gets_currencies, gets_party, gets_pairings
from transaction.states import StateChoices
from transaction.models import Invoices, workevents, workflowitems
from viewflow import fsm
from accounts.models import signatures


def gets_wf_item_id(id):
    return workflowitems.objects.get(id=id)


def upload_submit_transitions(request):
    user = request.user.party
    return signatures.objects.get(party=user, action__desc__contains="SUBMIT", model="UPLOAD")


class UploadFlow(object):
    # workitems = workflowitems()
    stage = fsm.State(StateChoices, default=StateChoices.STATUS_DRAFT)

    def __init__(self, workflowitems):
        self.workflowitems = workflowitems
        self.signatures = signatures

    @stage.setter()
    def _set_status_stage(self, value):
        self.workflowitems.initial_state = value

    @stage.getter()
    def _get_status(self):
        return self.workflowitems.initial_state

    @stage.transition(source=StateChoices.STATUS_DRAFT, target=StateChoices.STATUS_AWAITING_SIGN_A)
    def submit_draft(self, request):
        user = request.user
        ws = gets_wf_item_id(self.workflowitems.id)
        obj = upload_submit_transitions(request)

        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_COMPLETED
            self.workflowitems.action = "SUBMIT"

            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_COMPLETED, event_user=user, type="UPLOAD",
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_COMPLETED
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_COMPLETED, event_user=user, type="UPLOAD",
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_COMPLETED
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_COMPLETED, event_user=user, type="UPLOAD",
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_A, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def submit_A(self, request):
        user = request.user
        from_parties, to_parties = self.workflowitems.current_from_party, self.workflowitems.current_to_party
        ws = gets_wf_item_id(self.workflowitems.id)
        obj = upload_submit_transitions(request)

        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_COMPLETED
            self.workflowitems.final_state = StateChoices.STATUS_COMPLETED
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = []

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_COMPLETED, event_user=user, type="UPLOAD",
                                      interim_state=StateChoices.STATUS_COMPLETED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, c_final='YES')
            pg_type = self.workflowitems.uploads.program_type
            invoices_json = self.workflowitems.uploads.invoices
            for i in invoices_json:

                if pg_type == "APF":

                    invoice = Invoices.objects.create(program_type=pg_type, pairing=gets_pairings(i["buyerId"]), finance_currency_type=gets_currencies(i['financingCurrency']),
                                                      party=gets_party(i['counterparty_id']), invoice_currency=gets_currencies(i['invoiceType']), settlement_currency_type=gets_currencies(i['settlementCurrency']),
                                                      invoice_no=i['invoiceNo'],  amount=i['invoiceAmount'])

                    work = workflowitems.objects.create(
                        invoice=invoice, current_from_party=gets_party(i['counterparty_id']), current_to_party=gets_party(i['buyerName']), user=user, interim_state="AWAITING BUYER APPROVAL", final_state="AWAITING BUYER APPROVAL" )
                    work.save()

                    event = workevents.objects.create(
                        workitems=work, from_party=gets_party(i['counterparty_id']), to_party=gets_party(i['buyerName']), event_user=user, type="INVOICE", interim_state="AWAITING BUYER APPROVAL", to_state="AWAITING BUYER APPROVAL")
                    event.save()

                else:

                    invoice = Invoices.objects.create(program_type=pg_type, finance_currency_type=gets_currencies(i['financingCurrency']),
                                                      party=gets_party(i['counterparty_id']), invoice_currency=gets_currencies(i['invoiceType']), settlement_currency_type=gets_currencies(i['settlementCurrency']),
                                                      invoice_no=i['invoiceNo'],  amount=i['invoiceAmount'])

                    work = workflowitems.objects.create(
                        invoice=invoice, current_from_party=gets_party(i['counterparty_id']), current_to_party=gets_party(i['buyerName']), user=user, interim_state="FINANCE REQUESTED", final_state="FINANCE REQUESTED")
                    work.save()

                    event = workevents.objects.create(
                        workitems=work, from_party=gets_party(i['counterparty_id']), to_party=gets_party(i['buyerName']), event_user=user, type="INVOICE", interim_state="FINANCE REQUESTED", to_state="FINANCE REQUESTED")
                    event.save()

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_COMPLETED
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_COMPLETED, event_user=user, type="UPLOAD",
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_COMPLETED
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_COMPLETED, event_user=user, type="UPLOAD",
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_B, target=StateChoices.STATUS_AWAITING_SIGN_C)
    def submit_B(self, request):
        from_parties, to_parties = self.workflowitems.current_from_party, self.workflowitems.current_to_party
        user = request.user
        ws = gets_wf_item_id(self.workflowitems.id)
        obj = upload_submit_transitions(request)

        if (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):

            self.workflowitems.interim_state = StateChoices.STATUS_COMPLETED
            self.workflowitems.final_state = StateChoices.STATUS_COMPLETED
            self.workflowitems.initial_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = []

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, to_state=StateChoices.STATUS_COMPLETED, event_user=user, type="UPLOAD",
                                      interim_state=StateChoices.STATUS_COMPLETED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, c_final="YES")
            pg_type = self.workflowitems.uploads.program_type
            invoices_json = self.workflowitems.uploads.invoices
            for i in invoices_json:

                if pg_type == "APF":

                    invoice = Invoices.objects.create(program_type=pg_type, pairing=gets_pairings(i["buyerId"]), finance_currency_type=gets_currencies(i['financingCurrency']),
                                                      party=gets_party(i['counterparty_id']), invoice_currency=gets_currencies(i['invoiceType']), settlement_currency_type=gets_currencies(i['settlementCurrency']),
                                                      invoice_no=i['invoiceNo'],  amount=i['invoiceAmount'])

                    work = workflowitems.objects.create(
                        invoice=invoice, current_from_party=gets_party(i['counterparty_id']), current_to_party=gets_party(i['buyerName']), user=user, interim_state="AWAITING BUYER APPROVAL", final_state="AWAITING BUYER APPROVAL" )
                    work.save()

                    event = workevents.objects.create(
                        workitems=work, from_party=gets_party(i['counterparty_id']), to_party=gets_party(i['buyerName']), event_user=user, type="INVOICE", interim_state="AWAITING BUYER APPROVAL", to_state="AWAITING BUYER APPROVAL")
                    event.save()

                else:

                    invoice = Invoices.objects.create(program_type=pg_type, finance_currency_type=gets_currencies(i['financingCurrency']),
                                                      party=gets_party(i['counterparty_id']), invoice_currency=gets_currencies(i['invoiceType']), settlement_currency_type=gets_currencies(i['settlementCurrency']),
                                                      invoice_no=i['invoiceNo'],  amount=i['invoiceAmount'])

                    work = workflowitems.objects.create(
                        invoice=invoice, current_from_party=gets_party(i['counterparty_id']), current_to_party=gets_party(i['buyerName']), user=user, interim_state="FINANCE REQUESTED", final_state="FINANCE REQUESTED")
                    work.save()

                    event = workevents.objects.create(
                        workitems=work, from_party=gets_party(i['counterparty_id']), to_party=gets_party(i['buyerName']), event_user=user, type="INVOICE", interim_state="FINANCE REQUESTED", to_state="FINANCE REQUESTED")
                    event.save()

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_C
            self.workflowitems.final_state = StateChoices.STATUS_COMPLETED
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, to_state=StateChoices.STATUS_COMPLETED, user=user, type="UPLOAD",
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_C, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_C, target=StateChoices.STATUS_COMPLETED)
    def submit_C(self, request):
        user = request.user
        ws = gets_wf_item_id(self.workflowitems.id)
        from_parties, to_parties = self.workflowitems.current_from_party, self.workflowitems.current_to_party
        self.workflowitems.interim_state = StateChoices.STATUS_COMPLETED
        self.workflowitems.final_state = StateChoices.STATUS_COMPLETED
        self.workflowitems.action = "SUBMIT"
        self.workflowitems.next_available_transitions = []

        workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_C, to_state=StateChoices.STATUS_COMPLETED, event_user=user, type="UPLOAD",
                                  interim_state=StateChoices.STATUS_COMPLETED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, c_final="YES")

        pg_type = self.workflowitems.uploads.program_type
        invoices_json = self.workflowitems.uploads.invoices
        for i in invoices_json:

            if pg_type == "APF":

                invoice = Invoices.objects.create(program_type=pg_type, pairing=gets_pairings(i["buyerId"]), finance_currency_type=gets_currencies(i['financingCurrency']),
                                                  party=gets_party(i['counterparty_id']), invoice_currency=gets_currencies(i['invoiceType']), settlement_currency_type=gets_currencies(i['settlementCurrency']),
                                                  invoice_no=i['invoiceNo'],  amount=i['invoiceAmount'])

                work = workflowitems.objects.create(
                    invoice=invoice, current_from_party=gets_party(i['counterparty_id']), current_to_party=gets_party(i['buyerName']), user=user, interim_state="AWAITING BUYER APPROVAL", final_state="AWAITING BUYER APPROVAL" )
                work.save()

                event = workevents.objects.create(
                    workitems=work, from_party=gets_party(i['counterparty_id']), to_party=gets_party(i['buyerName']), event_user=user, type="INVOICE", interim_state="AWAITING BUYER APPROVAL", to_state="AWAITING BUYER APPROVAL")
                event.save()

            else:

                invoice = Invoices.objects.create(program_type=pg_type, finance_currency_type=gets_currencies(i['financingCurrency']),
                                                  party=gets_party(i['counterparty_id']), invoice_currency=gets_currencies(i['invoiceType']), settlement_currency_type=gets_currencies(i['settlementCurrency']),
                                                  invoice_no=i['invoiceNo'],  amount=i['invoiceAmount'])

                work = workflowitems.objects.create(
                    invoice=invoice, current_from_party=gets_party(i['counterparty_id']), current_to_party=gets_party(i['buyerName']), user=user, interim_state="FINANCE REQUESTED", final_state="FINANCE REQUESTED")
                work.save()

                event = workevents.objects.create(
                    workitems=work, from_party=gets_party(i['counterparty_id']), to_party=gets_party(i['buyerName']), event_user=user, type="INVOICE", interim_state="FINANCE REQUESTED", to_state="FINANCE REQUESTED")
                event.save()
