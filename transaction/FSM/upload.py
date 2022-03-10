from sre_parse import State
from urllib import request
from transaction.states import StateChoices
from transaction.models import Invoices, workevents, workflowitems
from viewflow import fsm
from accounts.models import Parties, User,  signatures


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
    def submit_draft(self):
        user = self.workflowitems.event_users
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="SUBMIT", model="UPLOAD")

        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_COMPLETED
            self.workflowitems.action = "SUBMIT"
            
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_COMPLETED, user = user, type = "UPLOAD" ,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_COMPLETED
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_COMPLETED,user = user,type = "UPLOAD" ,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_COMPLETED
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_COMPLETED,user = user,type = "UPLOAD" ,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_A, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def submit_A(self,request):
        user = self.workflowitems.event_users
        from_parties  = self.workflowitems.current_from_party
        to_parties = self.workflowitems.current_to_party 
        currency =  self.workflowitems.current_from_party.base_currency
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="SUBMIT", model="UPLOAD")

        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_COMPLETED
            self.workflowitems.final_state = StateChoices.STATUS_COMPLETED
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = []
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_COMPLETED,user = user,type = "UPLOAD" ,
                                      interim_state=StateChoices.STATUS_COMPLETED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, c_final='YES')
            cc = self.workflowitems.uploads.program_type
            gs = self.workflowitems.uploads.invoices
            if cc == "APF":
                invoice = Invoices.objects.create(party = gs.get('buyer_name'),invoice_no = gs.get('invoice_no'),program_type = cc , due_date = gs.get('due_date'),amount =  gs.get('invoice_amount'),finance_currency_type = currency , settlement_currency_type = currency )
                work = workflowitems.objects.create(
                invoice=invoice, current_from_party=from_parties ,current_to_party=to_parties , event_users=user,interim_state = "AWAITING BUYER APPROVAL",final_state = "AWAITING BUYER APPROVAL")
                work.save()
                event = workevents.objects.create(
                    workitems=work, from_party=gs.get('buyer_name'), to_party=gs.get('buyer_name'),user = user ,type = "INVOICE",interim_state = "AWAITING BUYER APPROVAL",to_state = "AWAITING BUYER APPROVAL")
                event.save()
            else:
                invoice = Invoices.objects.create(party = gs.get('buyer_name'),invoice_no = gs.get('invoice_no'),due_date = gs.get('due_date'), program_type = cc , amount =  gs.get('invoice_amount'),finance_currency_type = currency , settlement_currency_type = currency )
                work = workflowitems.objects.create(
                invoice=invoice, current_from_party=from_parties ,current_to_party=to_parties , event_users=user , interim_state = "FINANCE REQUESTED" , final_state = "FINANCE REQUESTED")
                work.save()
                event = workevents.objects.create(
                    workitems=work, from_party=gs.get('buyer_name'), to_party=gs.get('buyer_name'),user = user ,type = "INVOICE",interim_state = "FINANCE REQUESTED" , to_state = "FINANCE REQUESTED")
                event.save()
                


        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_COMPLETED
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_COMPLETED,user = user,type = "UPLOAD" ,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_COMPLETED
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_COMPLETED,user = user,type = "UPLOAD" ,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_B, target=StateChoices.STATUS_AWAITING_SIGN_C)
    def submit_B(self):
        from_parties  = self.workflowitems.current_from_party
        to_parties = self.workflowitems.current_to_party 
        currency =  self.workflowitems.current_from_party.base_currency
        user = self.workflowitems.event_users
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="SUBMIT", model="UPLOAD")

        if (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):

            self.workflowitems.interim_state = StateChoices.STATUS_COMPLETED
            self.workflowitems.final_state = StateChoices.STATUS_COMPLETED
            self.workflowitems.initial_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = []
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, to_state=StateChoices.STATUS_COMPLETED,user = user,type = "UPLOAD" ,
                                      interim_state=StateChoices.STATUS_COMPLETED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, c_final="YES")
            cc = self.workflowitems.uploads.program_type
            gs = self.workflowitems.uploads.invoices
            if cc == "APF":
                invoice = Invoices.objects.create(party = from_parties,invoice_no = gs.get('invoice_no'),program_type = cc , due_date = gs.get('due_date'),amount =  gs.get('invoice_amount'),finance_currency_type = currency , settlement_currency_type = currency )
                work = workflowitems.objects.create(
                invoice=invoice, current_from_party=from_parties ,current_to_party=to_parties , event_users=user,interim_state = "AWAITING BUYER APPROVAL",final_state = "AWAITING BUYER APPROVAL")
                work.save()
                event = workevents.objects.create(
                    workitems=work, from_party=from_parties, to_party=to_parties,user = user ,type = "INVOICE",interim_state = "AWAITING BUYER APPROVAL",to_state = "AWAITING BUYER APPROVAL")
                event.save()
            else:
                invoice = Invoices.objects.create(party = from_parties,invoice_no = gs.get('invoice_no'),program_type = cc , due_date = gs.get('due_date'),amount =  gs.get('invoice_amount'),finance_currency_type = currency , settlement_currency_type = currency )
                work = workflowitems.objects.create(
                invoice=invoice, current_from_party=from_parties ,current_to_party=to_parties , event_users=user , interim_state = "FINANCE REQUESTED" , final_state = "FINANCE REQUESTED")
                work.save()
                event = workevents.objects.create(
                    workitems=work, from_party=from_parties, to_party=to_parties,user = user ,type = "INVOICE",interim_state = "FINANCE REQUESTED" , to_state = "FINANCE REQUESTED")
                event.save()

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_C
            self.workflowitems.final_state = StateChoices.STATUS_COMPLETED
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_C]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, to_state=StateChoices.STATUS_COMPLETED,user = user,type = "UPLOAD" ,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_C, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_C, target=StateChoices.STATUS_COMPLETED)
    def submit_C(self):
        user = self.workflowitems.event_users
        from_parties  = self.workflowitems.current_from_party
        to_parties = self.workflowitems.current_to_party 
        currency =  self.workflowitems.current_from_party.base_currency
        self.workflowitems.interim_state = StateChoices.STATUS_COMPLETED
        self.workflowitems.final_state = StateChoices.STATUS_COMPLETED
        self.workflowitems.action = "SUBMIT"
        self.workflowitems.next_available_transitions = []
        ws = workflowitems.objects.get(id=self.workflowitems.id)
        workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_C, to_state=StateChoices.STATUS_COMPLETED,user = user,type = "UPLOAD" ,
                                  interim_state=StateChoices.STATUS_COMPLETED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, c_final="YES")
        cc = self.workflowitems.uploads.program_type
        gs = self.workflowitems.uploads.invoices
        if cc == "APF":
            invoice = Invoices.objects.create(party = from_parties,invoice_no = gs.get('invoice_no'),due_date = gs.get('due_date'),program_type = cc , amount =  gs.get('invoice_amount'),finance_currency_type = currency , settlement_currency_type = currency )
            work = workflowitems.objects.create(
            invoice=invoice, current_from_party=from_parties ,current_to_party=to_parties , event_users=user,interim_state = "AWAITING BUYER APPROVAL",final_state = "AWAITING BUYER APPROVAL")
            work.save()
            event = workevents.objects.create(
                workitems=work, from_party=from_parties, to_party=to_parties,user = user ,type = "INVOICE",interim_state = "AWAITING BUYER APPROVAL",to_state = "AWAITING BUYER APPROVAL")
            event.save()
        else:
            invoice = Invoices.objects.create(party = from_parties,invoice_no = gs.get('invoice_no'),due_date = gs.get('due_date'),program_type = cc , amount =  gs.get('invoice_amount'),finance_currency_type = currency , settlement_currency_type = currency )
            work = workflowitems.objects.create(
            invoice=invoice, current_from_party=from_parties ,current_to_party=to_parties , event_users=user , interim_state = "FINANCE REQUESTED" , final_state = "FINANCE REQUESTED")
            work.save()
            event = workevents.objects.create(
                workitems=work, from_party=from_parties, to_party=to_parties,user = user ,type = "INVOICE",interim_state = "FINANCE REQUESTED" , to_state = "FINANCE REQUESTED")
            event.save()