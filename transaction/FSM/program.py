from transaction.FSM.query_handler import (
    gets_wf_item_id ,
    accept_transition, 
    approve_transition, 
    submit_transition, 
    reject_transition,
    myuser,
)
from transaction.states import StateChoices
from transaction.models import Programs, workevents 
from viewflow import fsm
from accounts.models import Parties
import json

# VIEWFLOW CLASS

class WorkFlow(object):
    stage = fsm.State(StateChoices, default=StateChoices.STATUS_DRAFT)

    def __init__(self, workflowitems):
        self.workflowitems = workflowitems

    

    @stage.setter()
    def _set_status_stage(self, value):
        # locking the program for actions
        qs = self.workflowitems.program
        qs.is_locked = True
        qs.save()
        
        self.workflowitems.initial_state = value
        

    @stage.getter()
    def _get_status(self):
        return self.workflowitems.initial_state



# ---------------------#
# DELETE TRANSITION    #
# ---------------------#

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_DELETED)
    def delete(self,request):
        ws = gets_wf_item_id(self.workflowitems.id)
        user = request.user
        self.workflowitems.interim_state = self.workflowitems.final_state =  StateChoices.STATUS_DELETED
        self.workflowitems.current_from_party = self.workflowitems.current_to_party = self.workflowitems.user.party
        self.workflowitems.action = self.workflowitems.subaction = StateChoices.STATUS_DELETED
        self.workflowitems.next_available_transitions = None
        
        workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DELETED, to_state=StateChoices.STATUS_DELETED, action = StateChoices.STATUS_DELETED,subaction = StateChoices.STATUS_DELETED,  event_user=user, type="PROGRAM",end = 'YES',
                                  interim_state=StateChoices.STATUS_DELETED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, c_final="YES" )

# ---------------------#
# RETURN  TRANSITION   #
# ---------------------#

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_DRAFT)
    def returns(self, request):
        ws = gets_wf_item_id(self.workflowitems.id)
        user = request.user
        self.workflowitems.final_state = StateChoices.STATUS_DRAFT
        self.workflowitems.next_available_transitions = None
        self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
        self.workflowitems.action , self.workflowitems.subaction = StateChoices.RETURN , StateChoices.INITIAL_STATE
        workevents.objects.create(workitems=ws, from_state=self.workflowitems.interim_state, to_state=StateChoices.STATUS_DRAFT, event_user=user, type = 'PROGRAM' , action = StateChoices.RETURN,subaction = StateChoices.INITIAL_STATE, 
                                       interim_state=StateChoices.STATUS_DRAFT, from_party=user.party, to_party=user.party)
        self.workflowitems.interim_state = StateChoices.STATUS_DRAFT



# ---------------------#
# SUBMIT TRANSITION    #
# ---------------------#

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_DRAFT)
    def submit(self, request):
        user = request.user
        
        ws = gets_wf_item_id(self.workflowitems.id)
        obj = submit_transition(request)
        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.interim_state , self.workflowitems.final_state  = StateChoices.STATUS_AWAITING_SIGN_A , StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_A]
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.SUBMIT , StateChoices.MAKER
            
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_AW_APPROVAL, event_user=user,action = StateChoices.SUBMIT,subaction = StateChoices.MAKER,
                                           interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, type="PROGRAM", to_party=self.workflowitems.current_to_party)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state , self.workflowitems.final_state  = StateChoices.STATUS_AWAITING_SIGN_A , StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.SUBMIT , StateChoices.MAKER
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_AW_APPROVAL, event_user=user,action = StateChoices.SUBMIT,subaction = StateChoices.MAKER,
                                           interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, type="PROGRAM", to_party=self.workflowitems.current_to_party)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state , self.workflowitems.final_state  = StateChoices.STATUS_AWAITING_SIGN_A , StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.SUBMIT , StateChoices.MAKER
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_AW_APPROVAL, event_user=user,action = StateChoices.SUBMIT,subaction = StateChoices.MAKER,
                                           interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, type="PROGRAM", to_party=self.workflowitems.current_to_party)


    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_DRAFT)
    def submit_level_1(self, request):
        bank = Parties.objects.get(party_type="BANK")
        user = request.user
        ws = gets_wf_item_id(self.workflowitems.id)
        obj = submit_transition(request)

        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.interim_state = self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.next_available_transitions = None
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.SUBMIT , StateChoices.SIGN_A
            self.workflowitems.current_from_party = user.party
            cs = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, event_user=user, action = StateChoices.SUBMIT,subaction = StateChoices.SIGN_A,
                                           to_state=StateChoices.STATUS_AW_APPROVAL, interim_state=StateChoices.STATUS_AW_APPROVAL, from_party=self.workflowitems.current_from_party, type="PROGRAM", to_party=self.workflowitems.current_to_party)
            
            if user.party.party_type == "BANK":
                cs.c_final = cs.final = "YES"
                cs.to_party = self.workflowitems.user.party
                self.workflowitems.current_to_party = self.workflowitems.user.party
                cs.save()
            else:
                cs.final = "YES"
                self.workflowitems.current_to_party = bank
                cs.to_party = bank
                cs.save()

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state , self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_B , StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.SUBMIT , StateChoices.SIGN_A
            self.workflowitems.current_to_party = self.workflowitems.current_from_party = user.party
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_B]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, event_user=user,action = StateChoices.SUBMIT,subaction = StateChoices.SIGN_A,
                                      to_state=StateChoices.STATUS_AW_APPROVAL, interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, type="PROGRAM", to_party=self.workflowitems.current_to_party)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state , self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_B , StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.current_to_party = self.workflowitems.current_from_party = user.party
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.SUBMIT , StateChoices.SIGN_A
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, event_user=user,action = StateChoices.SUBMIT,subaction = StateChoices.SIGN_A,
                                      to_state=StateChoices.STATUS_AW_APPROVAL, interim_state=StateChoices.STATUS_AWAITING_SIGN_B, type="PROGRAM", from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_DRAFT)
    def submit_level_2(self, request):
        bank = Parties.objects.get(party_type="BANK")
        user = request.user
        ws = gets_wf_item_id(self.workflowitems.id)
        obj = submit_transition(request)

        if (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.next_available_transitions = None
            self.workflowitems.current_from_party = user.party
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.SUBMIT , StateChoices.SIGN_B

            cs = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, event_user=user, action = StateChoices.SUBMIT,subaction = StateChoices.SIGN_B,
                                           to_state=StateChoices.STATUS_AW_APPROVAL, interim_state=StateChoices.STATUS_AW_APPROVAL, type="PROGRAM", from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "BANK":
                cs.c_final = cs.final = "YES"
                cs.to_party = self.workflowitems.user.party
                self.workflowitems.current_to_party = self.workflowitems.user.party
                cs.save()
            else:
                cs.final = "YES"
                self.workflowitems.current_to_party = bank
                cs.to_party = bank
                cs.save()

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state, self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_C , StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.SUBMIT , StateChoices.SIGN_B
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, event_user=user,action = StateChoices.SUBMIT,subaction = StateChoices.SIGN_B,
                                      to_state=StateChoices.STATUS_AW_APPROVAL, interim_state=StateChoices.STATUS_AWAITING_SIGN_C, from_party=self.workflowitems.current_from_party, type="PROGRAM", to_party=self.workflowitems.current_to_party)


    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_DRAFT)
    def submit_level_3(self, request):
        bank = Parties.objects.get(party_type="BANK")
        user = request.user
        ws = gets_wf_item_id(self.workflowitems.id)
        self.workflowitems.interim_state = self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL
        self.workflowitems.next_available_transitions = None
        self.workflowitems.current_from_party = user.party
        self.workflowitems.action , self.workflowitems.subaction = StateChoices.SUBMIT , StateChoices.SIGN_C
        cs = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT,  event_user=user, action = StateChoices.SUBMIT,subaction = StateChoices.SIGN_C,
                                        to_state=StateChoices.STATUS_AW_APPROVAL, interim_state=StateChoices.STATUS_AW_APPROVAL, from_party=self.workflowitems.current_from_party, type="PROGRAM", to_party=self.workflowitems.current_to_party)
        
        if request.user.party.party_type == "BANK":
            cs.c_final = cs.final = "YES"
            cs.to_party = self.workflowitems.user.party
            self.workflowitems.current_to_party = self.workflowitems.user.party
            cs.save()
        else:
            cs.final = "YES"
            self.workflowitems.current_to_party = bank
            cs.to_party = bank
            cs.save()


# ---------------------#
# REJECT TRANSITION    #
# ---------------------#

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AW_ACCEPT)
    def reject(self, request):
        user = request.user
        ws = gets_wf_item_id(self.workflowitems.id)
        obj = reject_transition(request)
        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):

            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_A , StateChoices.STATUS_REJECTED
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_A]
            self.workflowitems.action ,self.workflowitems.subaction = StateChoices.REJECT , StateChoices.MAKER
            
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_ACCEPT, to_state=StateChoices.STATUS_REJECTED, event_user=user,action = StateChoices.REJECT,subaction = StateChoices.MAKER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, type="PROGRAM", to_party=self.workflowitems.current_to_party)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):

            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_A , StateChoices.STATUS_REJECTED
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]
            self.workflowitems.action ,self.workflowitems.subaction = StateChoices.REJECT , StateChoices.MAKER
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_ACCEPT, to_state=StateChoices.STATUS_REJECTED, event_user=user,action = StateChoices.REJECT,subaction = StateChoices.MAKER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, type="PROGRAM", to_party=self.workflowitems.current_to_party)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):

            self.workflowitems.interim_state,self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_A , StateChoices.STATUS_REJECTED
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.action ,self.workflowitems.subaction = StateChoices.REJECT , StateChoices.MAKER
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_ACCEPT, to_state=StateChoices.STATUS_REJECTED, event_user=user,action = StateChoices.REJECT,subaction = StateChoices.MAKER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, type="PROGRAM", to_party=self.workflowitems.current_to_party)


    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AW_ACCEPT)
    def reject_level_1(self, request):
        bank = Parties.objects.get(party_type="BANK")
        user = request.user
        ws = gets_wf_item_id(self.workflowitems.id)
        obj = reject_transition(request)

        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.interim_state = self.workflowitems.final_state = StateChoices.STATUS_REJECTED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.REJECT, StateChoices.SIGN_A
            self.workflowitems.current_from_party = user.party
            qs = self.workflowitems.program
            qs.is_locked = False
            qs.save()

            cs = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_ACCEPT, event_user=user,action = StateChoices.REJECT,subaction = StateChoices.SIGN_A,
                                           to_state=StateChoices.STATUS_REJECTED, interim_state=StateChoices.STATUS_REJECTED, type="PROGRAM", from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)
            
            if request.user.party.party_type == "BANK":
                cs.c_final = cs.final = cs.end = "YES"
                qs = self.workflowitems.program
                qs.is_locked = False
                qs.save()
                cs.to_party = self.workflowitems.user.party
                self.workflowitems.current_to_party = self.workflowitems.user.party
                cs.save()
            else:
                cs.final = "YES"
                self.workflowitems.current_to_party = bank
                cs.to_party = bank
                cs.save()

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state , self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_B , StateChoices.STATUS_REJECTED
            self.workflowitems.current_to_party = self.workflowitems.current_from_party = user.party
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_B]
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.REJECT, StateChoices.SIGN_A
            # self.workflowitems.program.is_locked = True

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_ACCEPT, event_user=user,action = StateChoices.REJECT,subaction = StateChoices.SIGN_A,
                                      to_state=StateChoices.STATUS_REJECTED, interim_state=StateChoices.STATUS_AWAITING_SIGN_B, type="PROGRAM", from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state , self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_B , StateChoices.STATUS_REJECTED
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.REJECT, StateChoices.SIGN_A
            self.workflowitems.current_to_party = self.workflowitems.current_from_party = user.party
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_ACCEPT, event_user=user,action = StateChoices.REJECT,subaction = StateChoices.SIGN_A,
                                      to_state=StateChoices.STATUS_REJECTED, interim_state=StateChoices.STATUS_AWAITING_SIGN_B, type="PROGRAM", from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AW_ACCEPT)
    def reject_level_2(self, request):
        bank = Parties.objects.get(party_type="BANK")
        user = request.user
        ws = gets_wf_item_id(self.workflowitems.id)
        obj = reject_transition(request)

        if (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = self.workflowitems.final_state = StateChoices.STATUS_REJECTED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.current_from_party = user.party
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.REJECT, StateChoices.SIGN_B
            self.workflowitems.program.is_locked = False
            qs = self.workflowitems.program
            qs.is_locked = False
            qs.save()

            cs = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_ACCEPT, event_user=user, action = StateChoices.REJECT,subaction = StateChoices.SIGN_B,
                                           to_state=StateChoices.STATUS_REJECTED, interim_state=StateChoices.STATUS_REJECTED, type="PROGRAM", from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)
            
            if request.user.party.party_type == "BANK":
                cs.c_final = cs.final = cs.end = "YES"
                cs.to_party = self.workflowitems.user.party
                self.workflowitems.current_to_party = self.workflowitems.user.party
                cs.save()
            else:
                cs.final = "YES"
                self.workflowitems.current_to_party = bank
                cs.to_party = bank
                cs.save()

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state, self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_C , StateChoices.STATUS_REJECTED
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.current_to_party = self.workflowitems.current_from_party = user.party
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.REJECT, StateChoices.SIGN_B
            self.workflowitems.program.is_locked = True

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_ACCEPT, event_user=user,action = StateChoices.REJECT,subaction = StateChoices.SIGN_B,
                                      to_state=StateChoices.STATUS_REJECTED, interim_state=StateChoices.STATUS_AWAITING_SIGN_C, type="PROGRAM", from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AW_ACCEPT)
    def reject_level_3(self, request):
        bank = Parties.objects.get(party_type="BANK")
        user = request.user
        ws = gets_wf_item_id(self.workflowitems.id)
        obj = reject_transition(request)

        if obj.sign_c == True:
            self.workflowitems.interim_state = self.workflowitems.final_state = StateChoices.STATUS_REJECTED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.current_from_party = user.party
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.REJECT, StateChoices.SIGN_C
            qs = self.workflowitems.program
            qs.is_locked = False
            qs.save()
            
            cs = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_ACCEPT, event_user=user, action = StateChoices.REJECT,subaction = StateChoices.SIGN_C,
                                           to_state=StateChoices.STATUS_REJECTED, interim_state=StateChoices.STATUS_REJECTED, type="PROGRAM", from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "BANK":
                cs.c_final = cs.final = cs.end = "YES"
                cs.to_party = self.workflowitems.user.party
                self.workflowitems.current_to_party = self.workflowitems.user.party
                cs.save()
            else:
                cs.final = "YES"
                self.workflowitems.current_to_party = bank
                cs.to_party = bank
                cs.save()


# ---------------------#
# ACCEPT TRANSITION    #
# ---------------------#

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AW_ACCEPT)
    def accept(self, request):
        user = request.user
        ws = gets_wf_item_id(self.workflowitems.id)
        obj = accept_transition(request)

        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):

            self.workflowitems.interim_state, self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_A ,StateChoices.STATUS_ACCEPTED
            self.workflowitems.current_to_party = self.workflowitems.current_from_party = user.party
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_A]
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.ACCEPT , StateChoices.MAKER
            
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_ACCEPT, to_state=StateChoices.STATUS_ACCEPTED, event_user=user, type="PROGRAM",action = StateChoices.ACCEPT,subaction = StateChoices.MAKER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):

            self.workflowitems.interim_state, self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_A ,StateChoices.STATUS_ACCEPTED
            self.workflowitems.current_to_party = self.workflowitems.current_from_party = user.party
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.ACCEPT , StateChoices.MAKER

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_ACCEPT, to_state=StateChoices.STATUS_ACCEPTED, event_user=user, type="PROGRAM",action = StateChoices.ACCEPT,subaction = StateChoices.MAKER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):

            self.workflowitems.interim_state, self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_A ,StateChoices.STATUS_ACCEPTED
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.current_to_party = self.workflowitems.current_from_party = user.party
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.ACCEPT , StateChoices.MAKER
            
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_ACCEPT, to_state=StateChoices.STATUS_ACCEPTED, event_user=user, type="PROGRAM",action = StateChoices.ACCEPT,subaction = StateChoices.MAKER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AW_ACCEPT)
    def accept_level_1(self, request):
        bank = Parties.objects.get(party_type="BANK")
        user = myuser(request)
        ws = gets_wf_item_id(self.workflowitems.id)
        obj = accept_transition(request)

        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.interim_state = self.workflowitems.final_state = StateChoices.STATUS_ACCEPTED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.ACCEPT , StateChoices.SIGN_A
            self.workflowitems.current_to_party = bank
            
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_ACCEPT, final='YES', event_user=user, type="PROGRAM", end='YES',action = StateChoices.ACCEPT,subaction = StateChoices.SIGN_A,
                                      to_state=StateChoices.STATUS_ACCEPTED, interim_state=StateChoices.STATUS_ACCEPTED, from_party=self.workflowitems.current_from_party, to_party=bank)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state, self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_B , StateChoices.STATUS_ACCEPTED
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.ACCEPT , StateChoices.SIGN_A
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_B]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_ACCEPT, event_user=user, type="PROGRAM",action = StateChoices.ACCEPT,subaction = StateChoices.SIGN_A,
                                      to_state=StateChoices.STATUS_ACCEPTED, interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state, self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_B , StateChoices.STATUS_ACCEPTED
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.ACCEPT , StateChoices.SIGN_A
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_ACCEPT, event_user=user, type="PROGRAM",action = StateChoices.ACCEPT,subaction = StateChoices.SIGN_A,
                                      to_state=StateChoices.STATUS_ACCEPTED, interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AW_ACCEPT)
    def accept_level_2(self, request):
        bank = Parties.objects.get(party_type="BANK")
        user = myuser(request)
        ws = gets_wf_item_id(self.workflowitems.id)
        obj = accept_transition(request)

        if (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = self.workflowitems.final_state = StateChoices.STATUS_ACCEPTED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.current_to_party = bank
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.ACCEPT , StateChoices.SIGN_B
            
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_ACCEPT, final='YES', event_user=user, type="PROGRAM", end = 'YES',action = StateChoices.ACCEPT,subaction = StateChoices.SIGN_B,
                                      to_state=StateChoices.STATUS_ACCEPTED, interim_state=StateChoices.STATUS_ACCEPTED, from_party=self.workflowitems.current_from_party, to_party=bank)


        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_C
            self.workflowitems.final_state = StateChoices.STATUS_ACCEPTED
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.ACCEPT , StateChoices.SIGN_B
            
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_ACCEPT, event_user=user, type="PROGRAM",action = StateChoices.ACCEPT,subaction = StateChoices.SIGN_B,
                                      to_state=StateChoices.STATUS_ACCEPTED, interim_state=StateChoices.STATUS_AWAITING_SIGN_C, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=StateChoices.STATUS_AW_ACCEPT, target=StateChoices.STATUS_ACCEPTED)
    def accept_level_3(self, request):
        bank = Parties.objects.get(party_type="BANK")
        user = myuser(request)
        ws = gets_wf_item_id(self.workflowitems.id)
        obj = accept_transition(request)

        if obj.sign_c == True:
            self.workflowitems.interim_state = self.workflowitems.final_state = StateChoices.STATUS_ACCEPTED
            self.workflowitems.current_to_party = bank
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.ACCEPT , StateChoices.SIGN_C

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_ACCEPT, final='YES', event_user=user, type="PROGRAM", action = StateChoices.ACCEPT,subaction = StateChoices.SIGN_C,
                                      to_state=StateChoices.STATUS_ACCEPTED, interim_state=StateChoices.STATUS_ACCEPTED, from_party=self.workflowitems.current_from_party, to_party=bank)
        return None


# ---------------------#
# APPROVE TRANSITION   #
# ---------------------#

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AW_APPROVAL)
    def approve(self, request):
        user = request.user
        ws = gets_wf_item_id(self.workflowitems.id)
        obj = approve_transition(request)

        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):

            self.workflowitems.interim_state, self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_A , StateChoices.STATUS_APPROVED
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_A]
            self.workflowitems.current_to_party = self.workflowitems.current_from_party = user.party
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.APPROVE , StateChoices.MAKER
            

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_APPROVAL, to_state=StateChoices.STATUS_APPROVED, event_user=user, type="PROGRAM",action = StateChoices.APPROVE,subaction = StateChoices.MAKER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):

            self.workflowitems.interim_state, self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_A , StateChoices.STATUS_APPROVED
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]
            self.workflowitems.current_to_party = self.workflowitems.current_from_party = user.party
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.APPROVE , StateChoices.MAKER

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_APPROVAL, to_state=StateChoices.STATUS_APPROVED, event_user=user, type="PROGRAM",action = StateChoices.APPROVE,subaction = StateChoices.MAKER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):

            self.workflowitems.interim_state, self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_A , StateChoices.STATUS_APPROVED
            self.workflowitems.current_to_party = self.workflowitems.current_from_party = user.party
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.APPROVE , StateChoices.MAKER

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_APPROVAL, to_state=StateChoices.STATUS_APPROVED, event_user=user, type="PROGRAM",action = StateChoices.APPROVE,subaction = StateChoices.MAKER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AW_APPROVAL)
    def approve_signA(self, request):
        bank = Parties.objects.get(party_type="BANK")
        user = request.user
        ws = gets_wf_item_id(self.workflowitems.id)
        obj = approve_transition(request)

        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):

            self.workflowitems.interim_state = self.workflowitems.final_state =  StateChoices.STATUS_APPROVED
            self.workflowitems.current_from_party, self.workflowitems.current_to_party = bank, self.workflowitems.user.party
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.APPROVE , StateChoices.SIGN_A
            qs = self.workflowitems.program
            qs.is_locked = False
            qs.save()

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_APPROVAL, to_state=StateChoices.STATUS_APPROVED, event_user=user, type="PROGRAM",  final = 'YES',action = StateChoices.APPROVE,subaction = StateChoices.SIGN_A,
                                      interim_state=StateChoices.STATUS_APPROVED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, c_final="YES")

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):

            self.workflowitems.interim_state , self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_B , StateChoices.STATUS_APPROVED
            self.workflowitems.current_to_party = self.workflowitems.current_from_party = user.party
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_B]
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.APPROVE , StateChoices.SIGN_A

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_APPROVAL, to_state=StateChoices.STATUS_APPROVED, event_user=user, type="PROGRAM",action = StateChoices.APPROVE,subaction = StateChoices.SIGN_A,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):

            self.workflowitems.interim_state , self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_B , StateChoices.STATUS_APPROVED  
            self.workflowitems.current_to_party = self.workflowitems.current_from_party = user.party
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.APPROVE , StateChoices.SIGN_A

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_APPROVAL, to_state=StateChoices.STATUS_APPROVED, event_user=user, type="PROGRAM",action = StateChoices.APPROVE,subaction = StateChoices.SIGN_A,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AW_APPROVAL)
    def approve_signB(self, request):
        bank = Parties.objects.get(party_type="BANK")
        user = request.user
        ws = gets_wf_item_id(self.workflowitems.id)
        obj = approve_transition(request)

        if (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):

            self.workflowitems.interim_state = self.workflowitems.final_state = StateChoices.STATUS_APPROVED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.current_from_party, self.workflowitems.current_to_party = bank, self.workflowitems.user.party
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.APPROVE , StateChoices.SIGN_B
            qs = self.workflowitems.program
            qs.is_locked = False
            qs.save()

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_APPROVAL, to_state=StateChoices.STATUS_APPROVED, event_user=user, type="PROGRAM",  final = 'YES',action = StateChoices.APPROVE,subaction = StateChoices.SIGN_B,
                                      interim_state=StateChoices.STATUS_APPROVED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, c_final='YES')

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):

            self.workflowitems.interim_state , self.workflowitems.final_state = StateChoices.STATUS_AWAITING_SIGN_C , StateChoices.STATUS_APPROVED
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.APPROVE , StateChoices.SIGN_B

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_APPROVAL, to_state=StateChoices.STATUS_APPROVED, event_user=user, type="PROGRAM",action = StateChoices.APPROVE,subaction = StateChoices.SIGN_B,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_C, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AW_APPROVAL)
    def approve_signC(self, request):
        bank = Parties.objects.get(party_type="BANK")
        user = request.user
        ws = gets_wf_item_id(self.workflowitems.id)
        obj = approve_transition(request)

        if (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):

            self.workflowitems.interim_state = self.workflowitems.final_state = StateChoices.STATUS_APPROVED
            self.workflowitems.current_from_party, self.workflowitems.current_to_party = bank, self.workflowitems.user.party
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action , self.workflowitems.subaction = StateChoices.APPROVE , StateChoices.SIGN_C
            qs = self.workflowitems.program
            qs.is_locked = False
            qs.save()

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_APPROVAL, to_state=StateChoices.STATUS_APPROVED, event_user=user, type="PROGRAM" ,  final = 'YES',action = StateChoices.APPROVE,subaction = StateChoices.SIGN_C,
                                      interim_state=StateChoices.STATUS_APPROVED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, c_final='YES')
        return None
