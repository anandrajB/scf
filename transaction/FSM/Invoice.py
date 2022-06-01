from transaction.states import StateChoices
from transaction.models import workevents, workflowitems
from viewflow import fsm
from accounts.models import signatures , Parties
from transaction.FSM.query_handler import (
    gets_wf_item_id ,
    invoice_approve_transition,
    invoice_reject_transition,
    invoice_submit_transition,
    reqFin_transition
)


class InvoiceFlow(object):
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



# ----------------------#
# RETURN  -- TRANSITION #
# ----------------------#

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_DRAFT)
    def Return_Invoice(self,request):
        user = request.user
        ws = gets_wf_item_id(self.workflowitems.id)
        self.workflowitems.final_state = StateChoices.STATUS_DRAFT
        self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
        self.workflowitems.action , self.workflowitems.subaction = StateChoices.RETURN , StateChoices.INITIAL_STATE
        cs = workevents.objects.create(workitems=ws, from_state=self.workflowitems.interim_state, to_state=StateChoices.STATUS_INITIAL_STATE, type="INVOICE", event_user = user , action = StateChoices.RETURN,subaction = StateChoices.INITIAL_STATE,
                                  interim_state=StateChoices.STATUS_DRAFT, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)
        cs.save()
        self.workflowitems.interim_state = StateChoices.STATUS_DRAFT



# ---------------------#
# APPROVE  TRANSITION  #
# ---------------------#


    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AWAITING_BUYER_APPROVAL)
    def approve_APF(self, request):
        user = request.user
        party = request.user.party
        obj = invoice_approve_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)
       

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True ):
            self.workflowitems.interim_state ,  self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_A , StateChoices.STATUS_APPROVED_BY_BUYER
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.APPROVE , StateChoices.MAKER
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_A]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_APPROVED_BY_BUYER, type="INVOICE", event_user=user,action = StateChoices.APPROVE,subaction = StateChoices.MAKER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True ):
            self.workflowitems.interim_state ,  self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_A , StateChoices.STATUS_APPROVED_BY_BUYER
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.APPROVE , StateChoices.MAKER
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_APPROVED_BY_BUYER, type="INVOICE", event_user=user,action = StateChoices.APPROVE,subaction = StateChoices.MAKER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True ):
            self.workflowitems.interim_state ,  self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_A , StateChoices.STATUS_APPROVED_BY_BUYER
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.APPROVE , StateChoices.MAKER
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_APPROVED_BY_BUYER, type="INVOICE", event_user=user,action = StateChoices.APPROVE,subaction = StateChoices.MAKER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AWAITING_BUYER_APPROVAL)
    def approve_APF_SignA(self, request):
        user = request.user
        obj = invoice_approve_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)
        
        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True ):
            self.workflowitems.interim_state = self.workflowitems.final_state = StateChoices.STATUS_APPROVED_BY_BUYER
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.APPROVE , StateChoices.SIGN_A
            self.workflowitems.next_available_transitions = []
            self.workflowitems.current_from_party , self.workflowitems.current_to_party = user.party , self.workflowitems.user.party

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_APPROVED_BY_BUYER, type="INVOICE",final = 'YES', event_user=user,action = StateChoices.APPROVE,subaction = StateChoices.SIGN_A,
                                           interim_state=StateChoices.STATUS_APPROVED_BY_BUYER, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True ):
            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_B , StateChoices.STATUS_APPROVED_BY_BUYER
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.APPROVE , StateChoices.SIGN_A
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_B]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_APPROVED_BY_BUYER, type="INVOICE", event_user=user,action = StateChoices.APPROVE,subaction = StateChoices.SIGN_A,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True ):
            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_B , StateChoices.STATUS_APPROVED_BY_BUYER
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.APPROVE , StateChoices.SIGN_A
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_APPROVED_BY_BUYER, type="INVOICE", event_user=user,action = StateChoices.APPROVE,subaction = StateChoices.SIGN_A,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AWAITING_BUYER_APPROVAL)
    def approve_APF_SignB(self, request):
        user = request.user
        obj = invoice_approve_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)
        

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True ):
            self.workflowitems.interim_state = self.workflowitems.final_state  = StateChoices.STATUS_APPROVED_BY_BUYER
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.APPROVE , StateChoices.SIGN_B
            self.workflowitems.next_available_transitions = []
            self.workflowitems.current_from_party = user.party
            self.workflowitems.current_to_party = self.workflowitems.user.party
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL,final = 'YES', to_state=StateChoices.STATUS_APPROVED_BY_BUYER, type="INVOICE", event_user=user,action = StateChoices.APPROVE,subaction = StateChoices.SIGN_B,
                                           interim_state=StateChoices.STATUS_APPROVED_BY_BUYER, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            # if user.party.party_type == "BUYER":
            #     cc.to_party = self.workflowitems.user.party
            #     cc.save()

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True ):
            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_C,StateChoices.STATUS_APPROVED_BY_BUYER
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.APPROVE , StateChoices.SIGN_B
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_APPROVED_BY_BUYER, type="INVOICE", event_user=user,action = StateChoices.APPROVE,subaction = StateChoices.SIGN_B,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_C, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AWAITING_BUYER_APPROVAL)
    def approve_APF_SignC(self, request):
        user = request.user
        obj = invoice_approve_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)
        
        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True ):
            self.workflowitems.interim_state = self.workflowitems.final_state = StateChoices.STATUS_APPROVED_BY_BUYER
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.APPROVE , StateChoices.SIGN_C
            self.workflowitems.next_available_transitions = []
            self.workflowitems.current_from_party = user.party
            self.workflowitems.current_to_party = self.workflowitems.user.party
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL,final = 'YES', to_state=StateChoices.STATUS_APPROVED_BY_BUYER, type="INVOICE", event_user=user,action = StateChoices.APPROVE,subaction = StateChoices.SIGN_C,
                                           interim_state=StateChoices.STATUS_APPROVED_BY_BUYER, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            # if user.party.party_type == "BUYER":
            #     cc.to_party = self.workflowitems.user.party
            #     cc.save()



# ---------------------#
# REJECT  TRANSITION   #
# ---------------------#


    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AWAITING_SIGN_A)
    def reject_APF(self, request):
        user = request.user
        obj = invoice_reject_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)
        

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True ):
            self.workflowitems.interim_state, self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_A , StateChoices.STATUS_REJECTED_BY_BUYER
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.REJECT , StateChoices.MAKER
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_A]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_REJECTED_BY_BUYER, type="INVOICE", event_user=user,action = StateChoices.REJECT,subaction = StateChoices.MAKER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True ):
            self.workflowitems.interim_state, self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_A , StateChoices.STATUS_REJECTED_BY_BUYER
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.REJECT , StateChoices.MAKER
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_REJECTED_BY_BUYER, type="INVOICE", event_user=user,action = StateChoices.REJECT,subaction = StateChoices.MAKER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True ):
            self.workflowitems.interim_state, self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_A , StateChoices.STATUS_REJECTED_BY_BUYER
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.REJECT , StateChoices.MAKER
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_REJECTED_BY_BUYER, type="INVOICE", event_user=user,action = StateChoices.REJECT,subaction = StateChoices.MAKER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def reject_APF_SignA(self, request):
        user = request.user
        obj = invoice_reject_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)
        
        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True ):
            self.workflowitems.interim_state = self.workflowitems.final_state =StateChoices.STATUS_REJECTED_BY_BUYER
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.REJECT , StateChoices.SIGN_A
            self.workflowitems.current_from_party = user.party
            self.workflowitems.current_to_party = self.workflowitems.user.party
            self.workflowitems.next_available_transitions = []

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_REJECTED_BY_BUYER,final = 'YES', type="INVOICE", event_user=user,action = StateChoices.REJECT,subaction = StateChoices.SIGN_A,
                                           interim_state=StateChoices.STATUS_REJECTED_BY_BUYER, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            # if user.party.party_type == "BUYER":
            #     cc.to_party = self.workflowitems.user.party
            #     cc.save()

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True ):
            self.workflowitems.interim_state, self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_B , StateChoices.STATUS_REJECTED_BY_BUYER
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.REJECT , StateChoices.SIGN_A
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_B]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_REJECTED_BY_BUYER, type="INVOICE", event_user=user,action = StateChoices.REJECT,subaction = StateChoices.SIGN_A,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True ):
            self.workflowitems.interim_state, self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_B , StateChoices.STATUS_REJECTED_BY_BUYER
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.REJECT , StateChoices.SIGN_A
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_REJECTED_BY_BUYER, type="INVOICE", event_user=user,action = StateChoices.REJECT,subaction = StateChoices.SIGN_A,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AWAITING_SIGN_C)
    def reject_APF_SignB(self, request):
        user = request.user
        obj = invoice_reject_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)
        

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True ):
            self.workflowitems.interim_state = self.workflowitems.final_state =StateChoices.STATUS_REJECTED_BY_BUYER
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.REJECT , StateChoices.SIGN_B
            self.workflowitems.current_from_party = user.party
            self.workflowitems.current_to_party = self.workflowitems.user.party
            self.workflowitems.next_available_transitions = []

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B,to_state=StateChoices.STATUS_REJECTED_BY_BUYER, type="INVOICE", event_user=user,action = StateChoices.REJECT,subaction = StateChoices.SIGN_B,
                                           interim_state=StateChoices.STATUS_REJECTED_BY_BUYER, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, final="YES")

            # if request.user.party.party_type == "BUYER":
            #     cc.to_party = self.workflowitems.user.party
            #     cc.save()

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True ):
            self.workflowitems.interim_state, self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_C , StateChoices.STATUS_REJECTED_BY_BUYER
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.REJECT , StateChoices.SIGN_B
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, to_state=StateChoices.STATUS_REJECTED_BY_BUYER, type="INVOICE", event_user=user,action = StateChoices.REJECT,subaction = StateChoices.SIGN_B,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_C, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_REJECTED_BY_BUYER)
    def reject_APF_SignC(self, request):
        user = request.user
        obj = invoice_reject_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)
        
        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True ):
            self.workflowitems.interim_state = self.workflowitems.final_state =StateChoices.STATUS_REJECTED_BY_BUYER
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.REJECT , StateChoices.SIGN_C
            self.workflowitems.current_from_party = user.party
            self.workflowitems.current_to_party = self.workflowitems.user.party
            self.workflowitems.next_available_transitions = []

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_C, to_state=StateChoices.STATUS_REJECTED_BY_BUYER, type="INVOICE", event_user=user,action = StateChoices.REJECT,subaction = StateChoices.SIGN_C,
                                           interim_state=StateChoices.STATUS_REJECTED_BY_BUYER, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, final="YES")

            # if request.user.party.party_type == "BUYER":
            #     cc.to_party = self.workflowitems.user.party
            #     cc.save()


# ------------------------------#
# REQUEST FINANCE  TRANSITION   #
# ------------------------------#

    # @stage.transition(source=stage.ANY, target=None)
    def REQ_FIN_APF(self, request):
        user = request.user
        obj = reqFin_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)
      

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_A , StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.REQUEST_FINANCE , StateChoices.MAKER
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_A]

            workevents.objects.create(workitems=ws, from_state=self.workflowitems.initial_state, to_state=StateChoices.STATUS_FINANCE_REQUESTED, type="INVOICE", event_user=user,action = StateChoices.REQUEST_FINANCE,subaction = StateChoices.MAKER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_A , StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.REQUEST_FINANCE , StateChoices.MAKER
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]

            workevents.objects.create(workitems=ws, from_state=self.workflowitems.initial_state, to_state=StateChoices.STATUS_FINANCE_REQUESTED, type="INVOICE", event_user=user,action = StateChoices.REQUEST_FINANCE,subaction = StateChoices.MAKER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_A , StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.REQUEST_FINANCE , StateChoices.MAKER
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=self.workflowitems.initial_state, to_state=StateChoices.STATUS_FINANCE_REQUESTED, type="INVOICE", event_user=user,action = StateChoices.REQUEST_FINANCE,subaction = StateChoices.MAKER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    # @stage.transition(source=stage.ANY, target=stage.ANY)
    def REQ_FIN_APF_SignA(self, request):
        user = request.user
        obj = reqFin_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)
        bank = Parties.objects.get(party_type="BANK")
        
        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.interim_state = self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.REQUEST_FINANCE , StateChoices.SIGN_A
            self.workflowitems.current_from_party = user.party
            self.workflowitems.current_to_party = bank
            self.workflowitems.next_available_transitions = []

            cc = workevents.objects.create(workitems=ws, from_state=self.workflowitems.initial_state, to_state=StateChoices.STATUS_FINANCE_REQUESTED, type="INVOICE", event_user=user,action = StateChoices.REQUEST_FINANCE,subaction = StateChoices.SIGN_A,
                                           interim_state=StateChoices.STATUS_FINANCE_REQUESTED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "SELLER":
                cc.final = "YES"
                cc.to_party = bank
                cc.save()

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.REQUEST_FINANCE , StateChoices.SIGN_A
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B]

            workevents.objects.create(workitems=ws, from_state=self.workflowitems.initial_state, to_state=StateChoices.STATUS_FINANCE_REQUESTED, type="INVOICE", event_user=user,action = StateChoices.REQUEST_FINANCE,subaction = StateChoices.SIGN_A,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.REQUEST_FINANCE , StateChoices.SIGN_A
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=self.workflowitems.initial_state, to_state=StateChoices.STATUS_FINANCE_REQUESTED, type="INVOICE", event_user=user,action = StateChoices.REQUEST_FINANCE,subaction = StateChoices.SIGN_A,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    # @stage.transition(source=stage.ANY, target=stage.ANY)
    def REQ_FIN_APF_SignB(self, request):
        user = request.user
        obj = reqFin_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)
        bank = Parties.objects.get(party_type="BANK")
        

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = self.workflowitems.final_state =StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.REQUEST_FINANCE , StateChoices.SIGN_B
            self.workflowitems.current_from_party = user.party
            self.workflowitems.current_to_party = bank
            self.workflowitems.next_available_transitions = []

            cc = workevents.objects.create(workitems=ws, from_state=self.workflowitems.initial_state, to_state=StateChoices.STATUS_FINANCE_REQUESTED, type="INVOICE", event_user=user,action = StateChoices.REQUEST_FINANCE,subaction = StateChoices.SIGN_B,
                                           interim_state=StateChoices.STATUS_FINANCE_REQUESTED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "SELLER":
                cc.final = "YES"
                cc.to_party = bank
                cc.save()

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_C , StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.REQUEST_FINANCE , StateChoices.SIGN_B
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=self.workflowitems.initial_state, to_state=StateChoices.STATUS_FINANCE_REQUESTED, type="INVOICE", event_user=user,action = StateChoices.REQUEST_FINANCE,subaction = StateChoices.SIGN_B,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_C, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    # @stage.transition(source=stage.ANY, target=stage.ANY)
    def REQ_FIN_APF_SignC(self, request):
        user = request.user
        obj = reqFin_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)
        bank = Parties.objects.get(party_type="BANK")
        

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.REQUEST_FINANCE , StateChoices.SIGN_C
            self.workflowitems.current_from_party = user.party
            self.workflowitems.current_to_party = bank
            self.workflowitems.next_available_transitions = []

            cc = workevents.objects.create(workitems=ws, from_state=self.workflowitems.initial_state, to_state=StateChoices.STATUS_FINANCE_REQUESTED, type="INVOICE", event_user=user,action = StateChoices.REQUEST_FINANCE,subaction = StateChoices.SIGN_C,
                                           interim_state=StateChoices.STATUS_FINANCE_REQUESTED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "SELLER":
                cc.final = "YES"
                cc.to_party = bank
                cc.save()


# ----------------------#
# SUBMIT   TRANSITION   #
# ----------------------#


    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_REJECTED_BY_BUYER)
    def Submit_APF(self, request):
        user = request.user
        obj = invoice_submit_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)
        

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True ):
            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_A,StateChoices.STATUS_AWAITING_BUYER_APPROVAL
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.SUBMIT , StateChoices.MAKER
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_REJECTED_BY_BUYER, to_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, type="INVOICE", event_user=user,action = StateChoices.SUBMIT,subaction = StateChoices.MAKER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True ):
            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_A,StateChoices.STATUS_AWAITING_BUYER_APPROVAL
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.SUBMIT , StateChoices.MAKER
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_REJECTED_BY_BUYER, to_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, type="INVOICE", event_user=user,action = StateChoices.SUBMIT,subaction = StateChoices.MAKER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True ):
            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_A,StateChoices.STATUS_AWAITING_BUYER_APPROVAL
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.SUBMIT , StateChoices.MAKER
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_REJECTED_BY_BUYER, to_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, type="INVOICE", event_user=user,action = StateChoices.SUBMIT,subaction = StateChoices.MAKER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_REJECTED_BY_BUYER)
    def Submit_APF_SignA(self, request):
        user = request.user
        party = request.user.party
        obj = invoice_submit_transition(request)
        
        ws = gets_wf_item_id(self.workflowitems.id)
        

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True ):
            self.workflowitems.interim_state = self.workflowitems.final_state = StateChoices.STATUS_AWAITING_BUYER_APPROVAL
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.SUBMIT , StateChoices.SIGN_A
            self.workflowitems.current_from_party = party
            self.workflowitems.current_to_party = self.workflowitems.invoice.pairing.program_id.party
            self.workflowitems.next_available_transitions = []

            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_REJECTED_BY_BUYER, to_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, final = 'YES',type="INVOICE", event_user=user,action = StateChoices.SUBMIT,subaction = StateChoices.SIGN_A,
                                           interim_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "SELLER":
                cc.to_party = self.workflowitems.invoice.pairing.program_id.party
                cc.save()

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True ):
            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_B,StateChoices.STATUS_AWAITING_BUYER_APPROVAL
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.SUBMIT , StateChoices.SIGN_A
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_B]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_REJECTED_BY_BUYER, to_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, type="INVOICE", event_user=user,action = StateChoices.SUBMIT,subaction = StateChoices.SIGN_A,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True ):
            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_B,StateChoices.STATUS_AWAITING_BUYER_APPROVAL
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.SUBMIT , StateChoices.SIGN_A
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_REJECTED_BY_BUYER, to_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, type="INVOICE", event_user=user,action = StateChoices.SUBMIT,subaction = StateChoices.SIGN_A,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_REJECTED_BY_BUYER)
    def Submit_APF_SignB(self, request):
        user = request.user
        party = request.user.party
        obj = invoice_submit_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)
        

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True ):
            self.workflowitems.interim_state = self.workflowitems.final_state =StateChoices.STATUS_AWAITING_BUYER_APPROVAL
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.SUBMIT , StateChoices.SIGN_B
            self.workflowitems.current_from_party = party
            self.workflowitems.current_to_party = self.workflowitems.invoice.pairing.program_id.party
            self.workflowitems.next_available_transitions = []

            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_REJECTED_BY_BUYER, to_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, type="INVOICE", final = 'YES',event_user=user,action = StateChoices.SUBMIT,subaction = StateChoices.SIGN_B,
                                           interim_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "SELLER":
                
                cc.to_party = self.workflowitems.invoice.pairing.program_id.party
                cc.save()

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True ):
            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_C,StateChoices.STATUS_AWAITING_BUYER_APPROVAL
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.SUBMIT , StateChoices.SIGN_B
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_REJECTED_BY_BUYER, to_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, type="INVOICE", event_user=user,action = StateChoices.SUBMIT,subaction = StateChoices.SIGN_B,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_C, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_REJECTED_BY_BUYER)
    def Submit_APF_SignC(self, request):
        user = request.user
        party = request.user.party
        obj = invoice_submit_transition(request)
        
        ws = gets_wf_item_id(self.workflowitems.id)
        

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True ):
            self.workflowitems.interim_state = self.workflowitems.final_state = StateChoices.STATUS_AWAITING_BUYER_APPROVAL
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.SUBMIT , StateChoices.SIGN_C
            self.workflowitems.current_from_party = party
            self.workflowitems.current_to_party = self.workflowitems.invoice.pairing.program_id.party
            self.workflowitems.next_available_transitions = []

            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_REJECTED_BY_BUYER, to_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, type="INVOICE",final = 'YES', event_user=user,action = StateChoices.SUBMIT,subaction = StateChoices.SIGN_C,
                                           interim_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "SELLER":
                cc.to_party = self.workflowitems.invoice.pairing.program_id.party
                cc.save()



# ----------------------#
# ARCHIVE   TRANSITION  #
# ----------------------#


    @stage.transition(source=[StateChoices.STATUS_REJECTED_BY_BUYER, StateChoices.STATUS_FINANCE_REQUESTED, StateChoices.STATUS_APPROVED_BY_BUYER], target=StateChoices.STATUS_AWAITING_SIGN_A)
    def Archive_APF(self,request):
        user = request.user
        ws = gets_wf_item_id(self.workflowitems.id)
        obj = signatures.objects.get(party=user.party, action__desc__contains="ARCHIVE", model="INVOICE")
        
        
        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True ):
            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_A , StateChoices.STATUS_ARCHIVED
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.ARCHIVE , StateChoices.MAKER
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_A]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_REJECTED_BY_BUYER, to_state=StateChoices.STATUS_ARCHIVED, type="INVOICE",action = StateChoices.ARCHIVE,subaction = StateChoices.MAKER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True ):
            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_A , StateChoices.STATUS_ARCHIVED
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.ARCHIVE , StateChoices.MAKER
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_REJECTED_BY_BUYER, to_state=StateChoices.STATUS_ARCHIVED, type="INVOICE",action = StateChoices.ARCHIVE,subaction = StateChoices.MAKER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True ):
            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_A , StateChoices.STATUS_ARCHIVED
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.ARCHIVE , StateChoices.MAKER
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
        
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_REJECTED_BY_BUYER, to_state=StateChoices.STATUS_ARCHIVED, type="INVOICE",action = StateChoices.ARCHIVE,subaction = StateChoices.MAKER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_A, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def Archive_APF_SignA(self,request):
        user = request.user
        ws = gets_wf_item_id(self.workflowitems.id)
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="ARCHIVE", model="INVOICE")
        
        
        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True ):
            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_B ,StateChoices.STATUS_ARCHIVED
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.ARCHIVE , StateChoices.SIGN_A
            self.workflowitems.next_available_transitions = []
            
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_ARCHIVED, type="INVOICE",action = StateChoices.ARCHIVE,subaction = StateChoices.SIGN_A,
                                      interim_state=StateChoices.STATUS_ARCHIVED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, final="YES")

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True ):
            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_B ,StateChoices.STATUS_ARCHIVED
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.ARCHIVE , StateChoices.SIGN_A
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B]
            
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_ARCHIVED, type="INVOICE",action = StateChoices.ARCHIVE,subaction = StateChoices.SIGN_A,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True ):
            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_B ,StateChoices.STATUS_ARCHIVED
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.ARCHIVE , StateChoices.SIGN_A
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_ARCHIVED, type="INVOICE",action = StateChoices.ARCHIVE,subaction = StateChoices.SIGN_A,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_B, target=StateChoices.STATUS_AWAITING_SIGN_C)
    def Archive_APF_SignB(self,request):
        user = request.user
        ws = gets_wf_item_id(self.workflowitems.id)
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="ARCHIVE", model="INVOICE")
        
        
        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True ):
            self.workflowitems.interim_state = self.workflowitems.final_state = StateChoices.STATUS_ARCHIVED
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.ARCHIVE , StateChoices.SIGN_B
            self.workflowitems.next_available_transitions = []

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, to_state=StateChoices.STATUS_ARCHIVED, type="INVOICE",action = StateChoices.ARCHIVE,subaction = StateChoices.SIGN_B,
                                      interim_state=StateChoices.STATUS_ARCHIVED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, final="YES")

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True ):
            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_C , StateChoices.STATUS_ARCHIVED
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.ARCHIVE , StateChoices.SIGN_B
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_C]
           
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, to_state=StateChoices.STATUS_ARCHIVED, type="INVOICE",action = StateChoices.ARCHIVE,subaction = StateChoices.SIGN_B,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_C, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_C, target=StateChoices.STATUS_ARCHIVED)
    def Archive_APF_SignC(self,request):
        user = request.user
        ws = gets_wf_item_id(self.workflowitems.id)
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="ARCHIVE", model="INVOICE")
        
        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True ):
            self.workflowitems.interim_state = self.workflowitems.final_state  = StateChoices.STATUS_ARCHIVED
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.ARCHIVE , StateChoices.SIGN_C
            self.workflowitems.next_available_transitions = []
            
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_C, to_state=StateChoices.STATUS_ARCHIVED, type="INVOICE",action = StateChoices.ARCHIVE,subaction = StateChoices.SIGN_C,
                                      interim_state=StateChoices.STATUS_ARCHIVED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, final="YES")




###########################################################################################################################

## <----------------------------------| RF and DF FLOW|--FOR INVOICE SUBMIT ------------------------------------------->  ##

###########################################################################################################################





    @stage.transition(source=StateChoices.STATUS_DRAFT, target=StateChoices.STATUS_AWAITING_SIGN_A)
    def submit__draft(self,request):
        user = request.user
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="SUBMIT", model="INVOICE")
        
        program_type = type.invoice.program_type

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True and (program_type == "RF" or program_type == "DF")):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_FINANCE_REQUESTED, type="INVOICE", user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True and (program_type == "RF" or program_type == "DF")):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_FINANCE_REQUESTED, type="INVOICE", user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True and (program_type == "RF" or program_type == "DF")):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_FINANCE_REQUESTED, type="INVOICE", user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_A, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def submit__SignA(self):
        user = self.workflowitems.event_users
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="SUBMIT", model="INVOICE")
        
        program_type = type.invoice.program_type

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True and (program_type == "RF" or program_type == "DF")):

            self.workflowitems.interim_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = []
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_FINANCE_REQUESTED, type="INVOICE", user=user,
                                      interim_state=StateChoices.STATUS_FINANCE_REQUESTED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, final="YES")

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True and (program_type == "RF" or program_type == "DF")):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_FINANCE_REQUESTED, type="INVOICE", user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True and (program_type == "RF" or program_type == "DF")):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_FINANCE_REQUESTED, type="INVOICE", user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_B, target=StateChoices.STATUS_AWAITING_SIGN_C)
    def submit__SignB(self):
        user = self.workflowitems.event_users
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="SUBMIT", model="INVOICE")
        
        program_type = type.invoice.program_type

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True and (program_type == "RF" or program_type == "DF")):

            self.workflowitems.interim_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = []
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, to_state=StateChoices.STATUS_FINANCE_REQUESTED, type="INVOICE", user=user,
                                      interim_state=StateChoices.STATUS_FINANCE_REQUESTED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, final="YES")

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True and (program_type == "RF" or program_type == "DF")):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_C
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_C]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, to_state=StateChoices.STATUS_FINANCE_REQUESTED, type="INVOICE", user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_C, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_C, target=StateChoices.STATUS_FINANCE_REQUESTED)
    def submit__SignC(self):
        user = self.workflowitems.event_users
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="SUBMIT", model="INVOICE")
        
        program_type = type.invoice.program_type

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True and (program_type == "RF" or program_type == "DF")):

            self.workflowitems.interim_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.SUBMIT , StateChoices.SIGN_C
            self.workflowitems.next_available_transitions = []
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_C, to_state=StateChoices.STATUS_FINANCE_REQUESTED, type="INVOICE", user=user,
                                      interim_state=StateChoices.STATUS_FINANCE_REQUESTED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, final="YES")



