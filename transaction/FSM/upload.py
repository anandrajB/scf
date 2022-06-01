from transaction.states import StateChoices
from transaction.models import Invoices, workevents, workflowitems
from viewflow import fsm
from accounts.models import signatures
from transaction.FSM.query_handler import (
    gets_wf_item_id ,
    upload_submit_transitions ,
    gets_currencies, 
    gets_party, 
    gets_pairings
)
from transaction.states import StateChoices



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



# ---------------------#
# RETURN  TRANSITION   #
# ---------------------#

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_DRAFT)
    def invoice_upload_returns(self, request):
        ws = gets_wf_item_id(self.workflowitems.id)
        user = request.user
        self.workflowitems.final_state = StateChoices.STATUS_DRAFT
        self.workflowitems.next_available_transitions = None
        self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
        self.workflowitems.action , self.workflowitems.subaction = StateChoices.RETURN , StateChoices.INITIAL_STATE
        workevents.objects.create(workitems=ws, from_state=self.workflowitems.interim_state, to_state=StateChoices.STATUS_DRAFT, event_user=user, type = 'UPLOAD' , action = StateChoices.RETURN,subaction = StateChoices.INITIAL_STATE,
                                       interim_state=StateChoices.STATUS_DRAFT, from_party=user.party, to_party=user.party)
        self.workflowitems.interim_state = StateChoices.STATUS_DRAFT


# ---------------------#
# SUBMIT  TRANSITION   #
# ---------------------#

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_DRAFT)
    def submit_draft(self, request):
        user = request.user
        ws = gets_wf_item_id(self.workflowitems.id)
        obj = upload_submit_transitions(request)

        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):

            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_A , StateChoices.STATUS_COMPLETED
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.SUBMIT , StateChoices.MAKER

            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_COMPLETED, event_user=user, type="UPLOAD",action = StateChoices.SUBMIT,subaction = StateChoices.MAKER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_A , StateChoices.STATUS_COMPLETED
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.SUBMIT , StateChoices.MAKER
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_COMPLETED, event_user=user, type="UPLOAD",action = StateChoices.SUBMIT,subaction = StateChoices.MAKER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_A , StateChoices.STATUS_COMPLETED
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.SUBMIT , StateChoices.MAKER
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_COMPLETED, event_user=user, type="UPLOAD",action = StateChoices.SUBMIT,subaction = StateChoices.MAKER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_DRAFT)
    def submit_A(self, request):
        user = request.user
        ws = gets_wf_item_id(self.workflowitems.id)
        obj = upload_submit_transitions(request)

        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.interim_state = self.workflowitems.final_state = StateChoices.STATUS_COMPLETED
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.SUBMIT , StateChoices.SIGN_A
            self.workflowitems.next_available_transitions = []

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_COMPLETED, event_user=user, type="UPLOAD",action = StateChoices.SUBMIT,subaction = StateChoices.SIGN_A,
                                      interim_state=StateChoices.STATUS_COMPLETED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, c_final='YES')
            
            pg_type = self.workflowitems.uploads.program_type
            invoices_json = self.workflowitems.uploads.invoices

            # lifecycle of finance_Request model starts here
            for i in invoices_json:

                if pg_type == "APF":

                    invoice = Invoices.objects.create(program_type=pg_type, pairing=gets_pairings(i["buyerId"]), finance_currency_type=gets_currencies(i['financingCurrency']),
                                                      party=gets_party(i['counterparty_id']), invoice_currency=gets_currencies(i['invoiceType']), settlement_currency_type=gets_currencies(i['settlementCurrency']),
                                                      invoice_no=i['invoiceNo'],  amount=i['invoiceAmount'])

                    work = workflowitems.objects.create(
                        invoice=invoice, current_from_party=gets_party(i['counterparty_id']), type="INVOICE", action = "SUBMIT" ,current_to_party=gets_party(i['buyerName']), user=user, interim_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, final_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL )
                    work.save()

                    event = workevents.objects.create(
                        workitems=work, from_party=gets_party(i['counterparty_id']), action = "SUBMIT" ,final = 'YES',to_party=gets_party(i['buyerName']), event_user=user, type="INVOICE", interim_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL)
                    event.save()

                else:

                    invoice = Invoices.objects.create(program_type=pg_type, finance_currency_type=gets_currencies(i['financingCurrency']),
                                                      party=gets_party(i['counterparty_id']), invoice_currency=gets_currencies(i['invoiceType']), settlement_currency_type=gets_currencies(i['settlementCurrency']),
                                                      invoice_no=i['invoiceNo'],  amount=i['invoiceAmount'])

                    work = workflowitems.objects.create(
                        invoice=invoice, current_from_party=gets_party(i['counterparty_id']), action = "SUBMIT" ,type="INVOICE",current_to_party=gets_party(i['buyerName']), user=user, interim_state=StateChoices.STATUS_FINANCE_REQUESTED, final_state=StateChoices.STATUS_FINANCE_REQUESTED)
                    work.save()

                    event = workevents.objects.create(
                        workitems=work, from_party=gets_party(i['counterparty_id']), action = "SUBMIT" ,final = 'YES',to_party=gets_party(i['buyerName']), event_user=user, type="INVOICE", interim_state=StateChoices.STATUS_FINANCE_REQUESTED, to_state=StateChoices.STATUS_FINANCE_REQUESTED)
                    event.save()

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_B , StateChoices.STATUS_COMPLETED
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.SUBMIT , StateChoices.SIGN_A
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_COMPLETED, event_user=user, type="UPLOAD",action = StateChoices.SUBMIT,subaction = StateChoices.SIGN_A,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_B , StateChoices.STATUS_COMPLETED
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.SUBMIT , StateChoices.SIGN_A
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_COMPLETED, event_user=user, type="UPLOAD",action = StateChoices.SUBMIT,subaction = StateChoices.SIGN_A,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_DRAFT)
    def submit_B(self, request):
        user = request.user
        ws = gets_wf_item_id(self.workflowitems.id)
        obj = upload_submit_transitions(request)

        if (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):

            self.workflowitems.interim_state = self.workflowitems.final_state  = StateChoices.STATUS_COMPLETED
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.SUBMIT , StateChoices.SIGN_B
            self.workflowitems.next_available_transitions = []

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_COMPLETED, event_user=user, type="UPLOAD",action = StateChoices.SUBMIT,subaction = StateChoices.SIGN_B,
                                      interim_state=StateChoices.STATUS_COMPLETED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, c_final="YES")
            pg_type = self.workflowitems.uploads.program_type
            invoices_json = self.workflowitems.uploads.invoices
            for i in invoices_json:

                if pg_type == "APF":

                    invoice = Invoices.objects.create(program_type=pg_type, pairing=gets_pairings(i["buyerId"]), finance_currency_type=gets_currencies(i['financingCurrency']),
                                                      party=gets_party(i['counterparty_id']), invoice_currency=gets_currencies(i['invoiceType']), settlement_currency_type=gets_currencies(i['settlementCurrency']),
                                                      invoice_no=i['invoiceNo'],  amount=i['invoiceAmount'])

                    work = workflowitems.objects.create(
                        invoice=invoice, current_from_party=gets_party(i['counterparty_id']),action = "SUBMIT" ,type="INVOICE", current_to_party=gets_party(i['buyerName']), user=user, interim_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, final_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL )
                    work.save()

                    event = workevents.objects.create(
                        workitems=work, from_party=gets_party(i['counterparty_id']), action = "SUBMIT",final = 'YES',to_party=gets_party(i['buyerName']), event_user=user, type="INVOICE", interim_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL)
                    event.save()

                else:

                    invoice = Invoices.objects.create(program_type=pg_type, finance_currency_type=gets_currencies(i['financingCurrency']),
                                                      party=gets_party(i['counterparty_id']), invoice_currency=gets_currencies(i['invoiceType']), settlement_currency_type=gets_currencies(i['settlementCurrency']),
                                                      invoice_no=i['invoiceNo'],  amount=i['invoiceAmount'])

                    work = workflowitems.objects.create(
                        invoice=invoice, current_from_party=gets_party(i['counterparty_id']),action = "SUBMIT" ,type="INVOICE", current_to_party=gets_party(i['buyerName']), user=user, interim_state=StateChoices.STATUS_FINANCE_REQUESTED, final_state=StateChoices.STATUS_FINANCE_REQUESTED)
                    work.save()

                    event = workevents.objects.create(
                        workitems=work, from_party=gets_party(i['counterparty_id']),action = "SUBMIT", final = 'YES',to_party=gets_party(i['buyerName']), event_user=user, type="INVOICE", interim_state=StateChoices.STATUS_FINANCE_REQUESTED, to_state=StateChoices.STATUS_FINANCE_REQUESTED)
                    event.save()

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):

            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_C , StateChoices.STATUS_COMPLETED
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.SUBMIT , StateChoices.SIGN_B
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_COMPLETED, event_user=user, type="UPLOAD",action = StateChoices.SUBMIT,subaction = StateChoices.SIGN_B,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_C, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_DRAFT)
    def submit_C(self, request):
        user = request.user
        ws = gets_wf_item_id(self.workflowitems.id)
       
        self.workflowitems.interim_state = self.workflowitems.final_state = StateChoices.STATUS_COMPLETED
        self.workflowitems.action , self.workflowitems.subaction = StateChoices.SUBMIT , StateChoices.SIGN_C
        self.workflowitems.next_available_transitions = []

        workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_COMPLETED, event_user=user, type="UPLOAD",action = StateChoices.SUBMIT,subaction = StateChoices.SIGN_C,
                                  interim_state=StateChoices.STATUS_COMPLETED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, c_final="YES")

        pg_type = self.workflowitems.uploads.program_type
        invoices_json = self.workflowitems.uploads.invoices
        for i in invoices_json:

            if pg_type == "APF":

                invoice = Invoices.objects.create(program_type=pg_type, pairing=gets_pairings(i["buyerId"]), finance_currency_type=gets_currencies(i['financingCurrency']),
                                                  party=gets_party(i['counterparty_id']), invoice_currency=gets_currencies(i['invoiceType']), settlement_currency_type=gets_currencies(i['settlementCurrency']),
                                                  invoice_no=i['invoiceNo'],  amount=i['invoiceAmount'])

                work = workflowitems.objects.create(
                    invoice=invoice, current_from_party=gets_party(i['counterparty_id']),action = "SUBMIT" , type="INVOICE",current_to_party=gets_party(i['buyerName']), user=user, interim_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, final_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL )
                work.save()

                event = workevents.objects.create(
                    workitems=work, from_party=gets_party(i['counterparty_id']), action = 'SUBMIT',final = 'YES', to_party=gets_party(i['buyerName']), event_user=user, type="INVOICE", interim_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL)
                event.save()

            else:

                invoice = Invoices.objects.create(program_type=pg_type, finance_currency_type=gets_currencies(i['financingCurrency']),
                                                  party=gets_party(i['counterparty_id']), invoice_currency=gets_currencies(i['invoiceType']), settlement_currency_type=gets_currencies(i['settlementCurrency']),
                                                  invoice_no=i['invoiceNo'],  amount=i['invoiceAmount'])

                work = workflowitems.objects.create(
                    invoice=invoice, current_from_party=gets_party(i['counterparty_id']),action = "SUBMIT" , type="INVOICE",current_to_party=gets_party(i['buyerName']), user=user, interim_state=StateChoices.STATUS_FINANCE_REQUESTED, final_state=StateChoices.STATUS_FINANCE_REQUESTED)
                work.save()

                event = workevents.objects.create(
                    workitems=work, from_party=gets_party(i['counterparty_id']), action = "SUBMIT", final = 'YES',to_party=gets_party(i['buyerName']), event_user=user, type="INVOICE", interim_state=StateChoices.STATUS_FINANCE_REQUESTED, to_state=StateChoices.STATUS_FINANCE_REQUESTED)
                event.save()
