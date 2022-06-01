# # django fsm flows using djano-viewflow package == 2.0a02

from transaction.states import StateChoices
from transaction.models import workevents, workflowitems
from viewflow import fsm
from accounts.models import signatures, Parties
from transaction.FSM.query_handler import (
    gets_wf_item_id,
    bank_reject_transition,
    bank_overdue_transition,
    bank_settle_transition,
    bank_approve_transition
)



class InvoiceBankFlow(object):
    # workitems = workflowitems()
    stage = fsm.State(StateChoices, default=StateChoices.STATUS_DRAFT)

    def __init__(self, workflowitems):
        self.workflowitems = workflowitems

    @stage.setter()
    def _set_status_stage(self, value):
        self.workflowitems.initial_state = value

    @stage.getter()
    def _get_status(self):
        return self.workflowitems.initial_state




# ------------------------#
#  RETURN_BANK TRANSITION #
# ------------------------#

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_DRAFT)
    def Return_Bank_Invoice(self,request):
        user = request.user
        ws = gets_wf_item_id(self.workflowitems.id)
        self.workflowitems.final_state = StateChoices.STATUS_DRAFT
        self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
        self.workflowitems.action , self.workflowitems.subaction = StateChoices.RETURN , StateChoices.INITIAL_STATE
        cs = workevents.objects.create(workitems=ws, from_state=self.workflowitems.interim_state, to_state=StateChoices.STATUS_INITIAL_STATE, type="INVOICE", event_user = user ,
                                  interim_state=StateChoices.STATUS_DRAFT, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)
        cs.save()
        self.workflowitems.interim_state = StateChoices.STATUS_DRAFT



# ----------------------#
# REJECT  -- TRANSITION #
# ----------------------#




    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AWAITING_SIGN_A)
    def reject_invoice(self, request):
        user = request.user
        obj = bank_reject_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
                
            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_A , StateChoices.STATUS_FINANCE_REJECTED
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.REJECT , StateChoices.MAKER
            self.workflowitems.current_to_party = self.workflowitems.current_from_party = user.party
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_A]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_FINANCE_REQUESTED, to_state=StateChoices.STATUS_FINANCE_REJECTED, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):

            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_A , StateChoices.STATUS_FINANCE_REJECTED
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.REJECT , StateChoices.MAKER
            self.workflowitems.current_to_party = self.workflowitems.current_from_party = user.party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_FINANCE_REQUESTED, to_state=StateChoices.STATUS_FINANCE_REJECTED, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):

            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_A , StateChoices.STATUS_FINANCE_REJECTED
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.REJECT , StateChoices.MAKER
            self.workflowitems.current_to_party = self.workflowitems.current_from_party = user.party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_FINANCE_REQUESTED, to_state=StateChoices.STATUS_FINANCE_REJECTED, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def reject_inv_signA(self, request):
        user = request.user
        obj = bank_reject_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.interim_state = self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REJECTED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.REJECT , StateChoices.SIGN_A
            self.workflowitems.current_from_party = user.party
            self.workflowitems.current_to_party = self.workflowitems.user.party

            cc = workevents.objects.create(
                workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, interim_state=StateChoices.STATUS_FINANCE_REJECTED, to_state=StateChoices.STATUS_FINANCE_REJECTED, type="INVOICE", event_user=user, 
                from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "BANK":
                
                cc.to_party = self.workflowitems.user.party
                cc.save()

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_B , StateChoices.STATUS_FINANCE_REJECTED
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_B]
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.REJECT , StateChoices.SIGN_A
            self.workflowitems.current_to_party = self.workflowitems.current_from_party = user.party

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, interim_state=StateChoices.STATUS_AWAITING_SIGN_B,
                                      final_state=StateChoices.STATUS_FINANCE_REJECTED, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_B , StateChoices.STATUS_FINANCE_REJECTED
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.REJECT , StateChoices.SIGN_A
            self.workflowitems.current_to_party = self.workflowitems.current_from_party = user.party

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, interim_state=StateChoices.STATUS_AWAITING_SIGN_B,
                                      final_state=StateChoices.STATUS_FINANCE_REJECTED, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_B, target=StateChoices.STATUS_AWAITING_SIGN_C)
    def reject_inv_signB(self, request):

        user = request.user
        obj = bank_reject_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REJECTED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.REJECT , StateChoices.SIGN_B 
            self.workflowitems.current_from_party = user.party
            self.workflowitems.current_to_party = self.workflowitems.user.party

            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, interim_state=StateChoices.STATUS_FINANCE_REJECTED,
                                           final_state=StateChoices.STATUS_FINANCE_REJECTED, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "BANK":
                
                cc.to_party = self.workflowitems.user.party
                cc.save()

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_C,StateChoices.STATUS_FINANCE_REJECTED
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.REJECT , StateChoices.SIGN_B
            self.workflowitems.current_to_party = self.workflowitems.current_from_party = user.party

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, interim_state=StateChoices.STATUS_AWAITING_SIGN_C,
                                      final_state=StateChoices.STATUS_FINANCE_REJECTED, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_C, target=StateChoices.STATUS_SETTLED)
    def reject_inv_signC(self, request):

        user = request.user
        party = request.user.party
        obj = bank_reject_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = self.workflowitems.final_state =  StateChoices.STATUS_FINANCE_REJECTED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.REJECT , StateChoices.SIGN_C
            self.workflowitems.current_from_party = party
            self.workflowitems.current_to_party = self.workflowitems.user.party

            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_C, interim_state=StateChoices.STATUS_FINANCE_REJECTED,
                                           final_state=StateChoices.STATUS_FINANCE_REJECTED, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "BANK":
                
                cc.to_party = self.workflowitems.user.party
                cc.save()




# ----------------------#
# APPROVE -- TRANSITION #
# ----------------------#




    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_FINANCE_REQUESTED)
    def approve_invoice(self, request):
        user = request.user
        obj = bank_approve_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):

            self.workflowitems.interim_state , self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_A , StateChoices.STATUS_FINANCED
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.APPROVE , StateChoices.MAKER
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_A]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_FINANCE_REQUESTED, to_state=StateChoices.STATUS_FINANCED, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):

            self.workflowitems.interim_state , self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_A , StateChoices.STATUS_FINANCED
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.APPROVE , StateChoices.MAKER
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_FINANCE_REQUESTED, to_state=StateChoices.STATUS_FINANCED, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):

            self.workflowitems.interim_state , self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_A , StateChoices.STATUS_FINANCED
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.APPROVE , StateChoices.MAKER
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_FINANCE_REQUESTED, to_state=StateChoices.STATUS_FINANCED, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_FINANCE_REQUESTED)
    def approve_inv_signA(self, request):

        user = request.user
        obj = bank_approve_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_FINANCED
            self.workflowitems.final_state = StateChoices.STATUS_FINANCED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.APPROVE , StateChoices.SIGN_A
            self.workflowitems.current_from_party = user.party
            self.workflowitems.current_to_party = self.workflowitems.user.party

            cc = workevents.objects.create(
                workitems=ws, from_state=StateChoices.STATUS_FINANCE_REQUESTED, interim_state=StateChoices.STATUS_FINANCED, to_state=StateChoices.STATUS_FINANCED, type="INVOICE", final = 'YES',event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "BANK":
                
                cc.to_party = self.workflowitems.user.party
                cc.save()

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_FINANCED
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B]
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.APPROVE , StateChoices.SIGN_A
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_FINANCE_REQUESTED, interim_state=StateChoices.STATUS_AWAITING_SIGN_B,
                                      to_state=StateChoices.STATUS_FINANCED, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_FINANCED
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.APPROVE , StateChoices.SIGN_A
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_FINANCE_REQUESTED, interim_state=StateChoices.STATUS_AWAITING_SIGN_B,
                                      to_state=StateChoices.STATUS_FINANCED, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_FINANCE_REQUESTED)
    def approve_inv_signB(self, request):

        user = request.user
        obj = bank_approve_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = self.workflowitems.final_state =  StateChoices.STATUS_FINANCED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.APPROVE , StateChoices.SIGN_B
            self.workflowitems.current_from_party = user.party
            self.workflowitems.current_to_party = self.workflowitems.user.party

            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_FINANCE_REQUESTED, interim_state=StateChoices.STATUS_FINANCED,
                                           to_state=StateChoices.STATUS_FINANCED, type="INVOICE", final ='YES',event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "BANK":
                
                cc.to_party = self.workflowitems.user.party
                cc.save()

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_C ,  StateChoices.STATUS_FINANCED
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.APPROVE , StateChoices.SIGN_B
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_FINANCE_REQUESTED, interim_state=StateChoices.STATUS_AWAITING_SIGN_C,
                                      to_state=StateChoices.STATUS_FINANCED, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_FINANCE_REQUESTED)
    def approve_inv_signC(self, request):

        user = request.user
        obj = bank_approve_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = self.workflowitems.final_state =  StateChoices.STATUS_FINANCED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.APPROVE , StateChoices.SIGN_C
            self.workflowitems.current_from_party = user.party
            self.workflowitems.current_to_party = self.workflowitems.user.party

            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_FINANCE_REQUESTED, interim_state=StateChoices.STATUS_FINANCED,
                                           to_state=StateChoices.STATUS_FINANCED, type="INVOICE", final = 'YES',event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "BANK":
                
                cc.to_party = self.workflowitems.user.party
                cc.save()



# ----------------------#
# SETTLE --  TRANSITION #
# ----------------------#



    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_SETTLED)
    def settle_invoice(self, request):
        user = request.user
        obj = bank_settle_transition(request)
        ws = workflowitems.objects.get(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):

            self.workflowitems.interim_state = self.workflowitems.final_state = StateChoices.STATUS_SETTLED
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.SETTLE , StateChoices.MAKER
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_FINANCED, to_state=StateChoices.STATUS_SETTLED, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_SETTLED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):

            self.workflowitems.interim_state = self.workflowitems.final_state = StateChoices.STATUS_SETTLED
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.SETTLE , StateChoices.MAKER
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_FINANCED, to_state=StateChoices.STATUS_SETTLED, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_SETTLED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):

            self.workflowitems.interim_state = self.workflowitems.final_state = StateChoices.STATUS_SETTLED
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.SETTLE , StateChoices.MAKER
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_FINANCED, to_state=StateChoices.STATUS_SETTLED, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_SETTLED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_A, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def settle_signA(self, request):

        user = request.user
        obj = bank_settle_transition(request)
        ws = workflowitems.objects.get(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.interim_state , self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REJECTED , StateChoices.STATUS_SETTLED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.SETTLE , StateChoices.SIGN_A
            self.workflowitems.current_from_party = user.party
            self.workflowitems.current_to_party = self.workflowitems.user.party

            cc = workevents.objects.create(
                workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, interim_state=StateChoices.STATUS_SETTLED, to_state=StateChoices.STATUS_SETTLED, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "BANK":
                
                cc.to_party = self.workflowitems.user.party
                cc.save()

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state , self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_B , StateChoices.STATUS_SETTLED
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B]
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.SETTLE , StateChoices.SIGN_A
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, interim_state=StateChoices.STATUS_AWAITING_SIGN_B,
                                      final_state=StateChoices.STATUS_SETTLED, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state , self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_B , StateChoices.STATUS_SETTLED
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.SETTLE , StateChoices.SIGN_A
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, interim_state=StateChoices.STATUS_AWAITING_SIGN_B,
                                      final_state=StateChoices.STATUS_SETTLED, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_B, target=StateChoices.STATUS_AWAITING_SIGN_C)
    def settle_signB(self, request):

        user = request.user
        obj = bank_settle_transition(request)
        ws = workflowitems.objects.get(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = self.workflowitems.final_state  = StateChoices.STATUS_SETTLED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.SETTLE , StateChoices.SIGN_B
            self.workflowitems.current_from_party = user.party
            self.workflowitems.current_to_party = self.workflowitems.user.party

            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, interim_state=StateChoices.STATUS_SETTLED,
                                           final_state=StateChoices.STATUS_SETTLED, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "BANK":
                
                cc.to_party = self.workflowitems.user.party
                cc.save()

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state , self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_C , StateChoices.STATUS_SETTLED
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.SETTLE , StateChoices.SIGN_B
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, interim_state=StateChoices.STATUS_AWAITING_SIGN_C,
                                      final_state=StateChoices.STATUS_SETTLED, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_C, target=StateChoices.STATUS_SETTLED)
    def settle_signC(self, request):

        user = request.user
        obj = bank_settle_transition(request)
        ws = workflowitems.objects.get(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = self.workflowitems.final_state  = StateChoices.STATUS_SETTLED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.SETTLE , StateChoices.SIGN_C
            self.workflowitems.current_from_party = user.party
            self.workflowitems.current_to_party = self.workflowitems.user.party

            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_C, interim_state=StateChoices.STATUS_SETTLED,
                                           final_state=StateChoices.STATUS_SETTLED, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "BANK":
                
                cc.to_party = self.workflowitems.user.party
                cc.save()




# ----------------------#
# OVERDUE -- TRANSITION #
# ----------------------#




    @stage.transition(source=StateChoices.STATUS_FINANCED, target=StateChoices.STATUS_OVERDUE)
    def overdue_invoice(self, request):
        user = request.user
        obj = bank_overdue_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):

            self.workflowitems.interim_state  = self.workflowitems.final_state = StateChoices.STATUS_OVERDUE
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.STATUS_OVERDUE , StateChoices.MAKER
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_FINANCED, to_state=StateChoices.STATUS_OVERDUE, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_OVERDUE, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):

            self.workflowitems.interim_state  = self.workflowitems.final_state = StateChoices.STATUS_OVERDUE
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.STATUS_OVERDUE , StateChoices.MAKER
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_FINANCED, to_state=StateChoices.STATUS_OVERDUE, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_OVERDUE, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):

            self.workflowitems.interim_state  = self.workflowitems.final_state = StateChoices.STATUS_OVERDUE
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.STATUS_OVERDUE , StateChoices.MAKER
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_FINANCED, to_state=StateChoices.STATUS_OVERDUE, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_OVERDUE, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)



    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_A, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def overdue_signA(self, request):

        user = request.user
        obj = bank_overdue_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REJECTED,StateChoices.STATUS_OVERDUE
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.STATUS_OVERDUE , StateChoices.SIGN_A
            self.workflowitems.current_from_party = user.party
            self.workflowitems.current_to_party = self.workflowitems.user.party

            cc = workevents.objects.create(
                workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, interim_state=StateChoices.STATUS_FINANCE_REJECTED, to_state=StateChoices.STATUS_OVERDUE, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "BANK":
                
                cc.to_party = self.workflowitems.user.party
                cc.save()

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_B , StateChoices.STATUS_OVERDUE
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B]
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.STATUS_OVERDUE , StateChoices.SIGN_A
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, interim_state=StateChoices.STATUS_AWAITING_SIGN_B,
                                      final_state=StateChoices.STATUS_OVERDUE, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_B , StateChoices.STATUS_OVERDUE
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.STATUS_OVERDUE , StateChoices.SIGN_A
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, interim_state=StateChoices.STATUS_AWAITING_SIGN_B,
                                      final_state=StateChoices.STATUS_SETTLED, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_B, target=StateChoices.STATUS_AWAITING_SIGN_C)
    def overdue_signB(self, request):

        user = request.user
        obj = bank_overdue_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state,self.workflowitems.final_state  = StateChoices.STATUS_FINANCE_REJECTED , StateChoices.STATUS_OVERDUE 
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.STATUS_OVERDUE , StateChoices.SIGN_B
            self.workflowitems.current_from_party = user.party
            self.workflowitems.current_to_party = self.workflowitems.user.party

            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, interim_state=StateChoices.STATUS_FINANCE_REJECTED,
                                           final_state=StateChoices.STATUS_OVERDUE, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "BANK":
                
                cc.to_party = self.workflowitems.user.party
                cc.save()

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state ,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_C , StateChoices.STATUS_OVERDUE
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.STATUS_OVERDUE , StateChoices.SIGN_B
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, interim_state=StateChoices.STATUS_AWAITING_SIGN_C,
                                      final_state=StateChoices.STATUS_OVERDUE, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_C, target=StateChoices.STATUS_OVERDUE)
    def overdue_signC(self, request):

        user = request.user
        obj = bank_overdue_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state,self.workflowitems.final_state  = StateChoices.STATUS_FINANCE_REJECTED , StateChoices.STATUS_OVERDUE 
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.STATUS_OVERDUE , StateChoices.SIGN_C
            self.workflowitems.current_from_party = user.party
            self.workflowitems.current_to_party = self.workflowitems.user.party

            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_C, interim_state=StateChoices.STATUS_FINANCE_REJECTED,
                                           final_state=StateChoices.STATUS_OVERDUE, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "BANK":
                
                cc.to_party = self.workflowitems.user.party
                cc.save()
