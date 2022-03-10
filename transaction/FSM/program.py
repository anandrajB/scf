# django fsm flows using djano-viewflow package == 2.0a02
from urllib import request
from transaction.states import StateChoices
from transaction.models import workevents, workflowitems
from viewflow import fsm
from accounts.models import Parties ,  signatures


# FUNCTION FOR GETTING CURRENT LOGGED-IN USER
def myuser(request):
        return request.user


# FUNCTION FOR SUBMIT SIGNATURES BASED ON USER_TYPE i.e., bank / customer
def submit_transition(request):
    user = request.user
    bank = Parties.objects.get(party_type="BANK")
    if user.party.party_type == "BANK":
        obj = signatures.objects.get(
                party=bank, action__desc__contains="SUBMIT", model="PROGRAM")
    else :
        obj = signatures.objects.get(
                party=user.party, action__desc__contains="SUBMIT", model="PROGRAM")
    return obj
    


# FUNCTION FOR REJECT SIGNATURES BASED ON USER_TYPE i.e ., bank / customer
def reject_transition(request):
    user = request.user
    bank = Parties.objects.get(party_type="BANK")
    if user.party.party_type == "BANK":
        obj = signatures.objects.get(
                party=bank, action__desc__contains="REJECT", model="PROGRAM")
    else :
        obj = signatures.objects.get(
                party=user.party, action__desc__contains="REJECT", model="PROGRAM")
    return obj



# VIEWFLOW CLASS

class WorkFlow(object):
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



# --------------------------------------------------------------------------------------------------
# SUBMIT TRANSITION
# --------------------------------------------------------------------------------------------------
    
    @stage.transition(source=[StateChoices.STATUS_DRAFT, StateChoices.STATUS_AW_ACCEPT], target=StateChoices.STATUS_AWAITING_SIGN_A)
    def submit(self,request):
        user = request.user
        party = request.user.party
        obj = submit_transition(request)
        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.initial_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A]
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.action = 'SUBMIT'
            self.workflowitems.subaction = StateChoices.SUBMIT
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_AW_APPROVAL,event_user =  user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, type = "PROGRAM",to_party = self.workflowitems.current_to_party)

        
        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.initial_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.action = 'SUBMIT'
            self.workflowitems.subaction = StateChoices.SUBMIT
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_AW_APPROVAL, event_user = user ,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party,type = "PROGRAM", to_party=self.workflowitems.current_to_party)

       

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.action = 'SUBMIT'
            self.workflowitems.subaction = StateChoices.SUBMIT
            self.workflowitems.initial_state = StateChoices.STATUS_AWAITING_SIGN_A
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_AW_APPROVAL, event_user = user ,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, type = "PROGRAM",to_party=self.workflowitems.current_to_party)

    
        

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_A, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def submit_level_1(self,request):
        user = request.user
        party = request.user.party
        bank = Parties.objects.get(party_type="BANK")
        obj = submit_transition(request)
        
        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action = 'SUBMIT'
            self.workflowitems.subaction = StateChoices.SIGN_A
            self.workflowitems.current_from_party = party
            self.workflowitems.initial_state = StateChoices.STATUS_AW_ACCEPT
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            cs = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, event_user = user , 
                                      to_state=StateChoices.STATUS_AW_APPROVAL, interim_state=StateChoices.STATUS_AW_APPROVAL, from_party=self.workflowitems.current_from_party, type = "PROGRAM",to_party=self.workflowitems.current_to_party)
            if request.user.party.party_type  == "BANK":
                cs.c_final = "YES"
                cs.to_party = self.workflowitems.user.party
                self.workflowitems.current_to_party = self.workflowitems.user.party
                cs.save()
            else:
                cs.final = "YES"
                self.workflowitems.current_to_party = bank
                cs.to_party = bank
                cs.save()
        

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.action = 'SUBMIT'
            self.workflowitems.initial_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.subaction = StateChoices.SIGN_A
            self.workflowitems.current_to_party = self.workflowitems.current_from_party = party
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_B]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, event_user = user , 
                                      to_state=StateChoices.STATUS_AW_APPROVAL, interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party,type = "PROGRAM", to_party=self.workflowitems.current_to_party)

        
        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.initial_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.current_to_party = self.workflowitems.current_from_party = party
            self.workflowitems.subaction = StateChoices.SIGN_A
            self.workflowitems.action = 'SUBMIT'
            self.workflowitems.next_available_transitions = [StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, event_user = user , 
                                      to_state=StateChoices.STATUS_AW_APPROVAL, interim_state=StateChoices.STATUS_AWAITING_SIGN_B, type = "PROGRAM",from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_B, target=StateChoices.STATUS_AWAITING_SIGN_C)
    def submit_level_2(self,request):
        user = request.user
        party = request.user.party
        bank = Parties.objects.get(party_type="BANK")
        obj = submit_transition(request)

       

        if (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.next_available_transitions = []
            self.workflowitems.subaction = StateChoices.SIGN_B
            self.workflowitems.current_from_party = party
            self.workflowitems.action = 'SUBMIT'
            self.workflowitems.initial_state = StateChoices.STATUS_AW_ACCEPT
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            cs = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, event_user = user , 
                                      to_state=StateChoices.STATUS_AW_APPROVAL, interim_state=StateChoices.STATUS_AW_APPROVAL, type = "PROGRAM",from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)
            
            if request.user.party.party_type  == "BANK":
                cs.c_final = "YES"
                cs.to_party = self.workflowitems.user.party
                self.workflowitems.current_to_party = self.workflowitems.user.party
                cs.save()
            else:
                cs.final = "YES"
                self.workflowitems.current_to_party = bank
                cs.to_party = bank
                cs.save()
       

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_C
            self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.subaction = StateChoices.SIGN_B
            self.workflowitems.action = 'SUBMIT'
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, event_user = user , 
                                      to_state=StateChoices.STATUS_AW_APPROVAL, interim_state=StateChoices.STATUS_AWAITING_SIGN_C, from_party=self.workflowitems.current_from_party, type = "PROGRAM",to_party=self.workflowitems.current_to_party)


    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_C, target=StateChoices.STATUS_AW_APPROVAL)
    def submit_level_3(self,request):
        party = request.user.party
        bank = Parties.objects.get(party_type="BANK")
        user = request.user
        self.workflowitems.interim_state = StateChoices.STATUS_AW_APPROVAL
        self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL
        self.workflowitems.initial_state = StateChoices.STATUS_AW_ACCEPT
        self.workflowitems.next_available_transitions = []
        self.workflowitems.action = 'SUBMIT'
        self.workflowitems.current_from_party = party
        self.workflowitems.subaction = StateChoices.SIGN_C
        ws = workflowitems.objects.get(id=self.workflowitems.id)
        cs = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_C,  event_user = user,
                                  to_state=StateChoices.STATUS_AW_APPROVAL, interim_state=StateChoices.STATUS_AW_APPROVAL, from_party=self.workflowitems.current_from_party, type = "PROGRAM",to_party=self.workflowitems.current_to_party)
        if request.user.party.party_type  == "BANK":
            cs.c_final = "YES"
            cs.to_party = self.workflowitems.user.party
            self.workflowitems.current_to_party = self.workflowitems.user.party
            cs.save()
        else:
            cs.final = "YES"
            self.workflowitems.current_to_party = bank
            cs.to_party = bank
            cs.save()


# -------------------------------------------------------------------------------------------------
# REJECT TRANSITIONS
# --------------------------------------------------------------------------------------------------
    

    @stage.transition(source=StateChoices.STATUS_AW_ACCEPT, target=StateChoices.STATUS_AWAITING_SIGN_A)
    def reject(self,request):
        user = request.user
        party = request.user.party
        obj = reject_transition(request)
        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED
            self.workflowitems.initial_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A]
            self.workflowitems.action = 'REJECT'
            self.workflowitems.subaction = StateChoices.MAKER
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_ACCEPT, to_state=StateChoices.STATUS_REJECTED, event_user = user , 
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party,type = "PROGRAM", to_party=self.workflowitems.current_to_party)

       

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED
            self.workflowitems.initial_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]
            self.workflowitems.action = 'REJECT'
            self.workflowitems.subaction = StateChoices.MAKER
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_ACCEPT, to_state=StateChoices.STATUS_REJECTED, event_user =  user , 
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party,type = "PROGRAM", to_party=self.workflowitems.current_to_party)

        

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.initial_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.action = 'REJECT'
            self.workflowitems.subaction = StateChoices.MAKER
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_ACCEPT, to_state=StateChoices.STATUS_REJECTED, event_user = user , 
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, type = "PROGRAM",to_party=self.workflowitems.current_to_party)


    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_A, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def reject_level_1(self,request):
        user = request.user
        party = request.user.party
        bank = Parties.objects.get(party_type="BANK")
        obj = reject_transition(request)
        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_REJECTED
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.subaction = "SIGN_A"
            self.workflowitems.current_from_party = party
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            cs = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, event_user = user , 
                                      to_state=StateChoices.STATUS_REJECTED, interim_state=StateChoices.STATUS_REJECTED, type = "PROGRAM",from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)
            if request.user.party.party_type  == "BANK":
                cs.c_final = "YES"
                cs.to_party = self.workflowitems.user.party
                self.workflowitems.current_to_party = self.workflowitems.user.party
                cs.save()
            else:
                cs.final = "YES"
                self.workflowitems.current_to_party = bank
                cs.to_party = bank
                cs.save()
        

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED
            self.workflowitems.initial_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.current_to_party = self.workflowitems.current_from_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B]
            self.workflowitems.action = 'REJECT'
            self.workflowitems.initial_state = StateChoices.STATUS_AW_ACCEPT
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A,event_user = user , 
                                      to_state=StateChoices.STATUS_REJECTED, interim_state=StateChoices.STATUS_AWAITING_SIGN_B,type = "PROGRAM", from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

       
        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED
            self.workflowitems.initial_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.current_to_party = self.workflowitems.current_from_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, event_user = user , 
                                      to_state=StateChoices.STATUS_REJECTED, interim_state=StateChoices.STATUS_AWAITING_SIGN_B, type = "PROGRAM",from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_B, target=StateChoices.STATUS_AWAITING_SIGN_C)
    def reject_level_2(self,request):
        user = request.user
        party = request.user.party
        bank = Parties.objects.get(party_type="BANK")
        obj = reject_transition(request)
        
        if (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_REJECTED
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.current_from_party = party
            self.workflowitems.subaction = StateChoices.SIGN_B
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            cs = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, event_user = user,
                                      to_state=StateChoices.STATUS_REJECTED, interim_state=StateChoices.STATUS_REJECTED, type = "PROGRAM",from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)
            if request.user.party.party_type == "BANK":
                cs.c_final = "YES"
                cs.to_party = self.workflowitems.user.party
                self.workflowitems.current_to_party = self.workflowitems.user.party
                cs.save()
            else:
                cs.final = "YES"
                self.workflowitems.current_to_party = bank
                cs.to_party = bank
                cs.save()

       
        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_C
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.current_to_party = self.workflowitems.current_from_party = party
            self.workflowitems.subaction = StateChoices.SIGN_B
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, event_user = user , 
                                      to_state=StateChoices.STATUS_AW_APPROVAL, interim_state=StateChoices.STATUS_AWAITING_SIGN_C,type = "PROGRAM", from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_C, target=StateChoices.STATUS_REJECTED)
    def reject_level_3(self,request):
        user = request.user
        party = request.user.party
        bank = Parties.objects.get(party_type="BANK")
        obj = reject_transition(request)
        if obj.sign_c == True:
            self.workflowitems.interim_state = StateChoices.STATUS_REJECTED
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.current_from_party = party
            self.workflowitems.action = 'REJECT'
            self.workflowitems.subaction = StateChoices.SIGN_C
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            cs = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_C, event_user = user , 
                                      to_state=StateChoices.STATUS_AW_APPROVAL, interim_state=StateChoices.STATUS_AW_APPROVAL,type = "PROGRAM", from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)
           
            if request.user.is_administrator == True:
                cs.c_final = "YES"
                cs.to_party = self.workflowitems.user.party
                self.workflowitems.current_to_party = self.workflowitems.user.party
                cs.save()
            else:
                cs.final = "YES"
                self.workflowitems.current_to_party = bank
                cs.to_party = bank
                cs.save()

    
# -------------------------------------------------------------------------------------------------
# ACCEPT TRANSITION
# --------------------------------------------------------------------------------------------------

    @stage.transition(source=StateChoices.STATUS_AW_ACCEPT, target=StateChoices.STATUS_AWAITING_SIGN_A)
    def accept(self,request):
        user = request.user
        party = request.user.party
        bank = Parties.objects.get(party_type="BANK")
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="ACCEPT", model="PROGRAM")

        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_ACCEPTED
            self.workflowitems.initial_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.current_to_party = self.workflowitems.current_from_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A]
            self.workflowitems.action = 'ACCEPT'
            self.workflowitems.subaction = StateChoices.MAKER
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_ACCEPT, to_state=StateChoices.STATUS_ACCEPTED, event_user = user , type = "PROGRAM",
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_ACCEPTED
            self.workflowitems.initial_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.current_to_party = self.workflowitems.current_from_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]
            self.workflowitems.action = 'ACCEPT'
            self.workflowitems.subaction = StateChoices.MAKER
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_ACCEPTED, event_user = user , type = "PROGRAM",
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

       

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_ACCEPTED
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.action = 'ACCEPT'
            self.workflowitems.current_to_party = self.workflowitems.current_from_party = party
            self.workflowitems.subaction = StateChoices.MAKER
            self.workflowitems.initial_state = StateChoices.STATUS_AWAITING_SIGN_A
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_ACCEPTED, event_user = user , type = "PROGRAM",
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_A, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def accept_level_1(self,request):
        user = myuser(request)
        bank = Parties.objects.get(party_type="BANK")
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="ACCEPT", model="PROGRAM")

        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_ACCEPTED
            self.workflowitems.final_state = StateChoices.STATUS_ACCEPTED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action = 'ACCEPT'
            self.workflowitems.current_to_party = bank
            self.workflowitems.subaction = StateChoices.SIGN_A
            self.workflowitems.initial_state = StateChoices.STATUS_AW_ACCEPT
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, final='YES', event_user = user , type = "PROGRAM",
                                      to_state=StateChoices.STATUS_ACCEPTED, interim_state=StateChoices.STATUS_ACCEPTED, from_party=self.workflowitems.current_from_party, to_party=bank)


        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_ACCEPTED
            self.workflowitems.action = 'ACCEPT'
            self.workflowitems.initial_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.subaction = StateChoices.SIGN_A
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B]
            # self.workflowitems.initial_state = StateChoices.STATUS_AW_ACCEPT
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, event_user = user , type = "PROGRAM",
                                      to_state=StateChoices.STATUS_ACCEPTED, interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_ACCEPTED
            self.workflowitems.initial_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.subaction = StateChoices.SIGN_A
            self.workflowitems.action = 'ACCEPT'
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, event_user = user , type = "PROGRAM",
                                      to_state=StateChoices.STATUS_ACCEPTED, interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_B, target=StateChoices.STATUS_AWAITING_SIGN_C)
    def accept_level_2(self,request):
        user = myuser(request)
        bank = Parties.objects.get(party_type="BANK")
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="ACCEPT", model="PROGRAM")

    
        if (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_ACCEPTED
            self.workflowitems.final_state = StateChoices.STATUS_ACCEPTED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.subaction = StateChoices.SIGN_B
            self.workflowitems.current_to_party = bank
            self.workflowitems.action = 'ACCEPT'
            self.workflowitems.initial_state = StateChoices.STATUS_AW_ACCEPT
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, final='YES', event_user = user , type = "PROGRAM",
                                      to_state=StateChoices.STATUS_ACCEPTED, interim_state=StateChoices.STATUS_ACCEPTED, from_party=self.workflowitems.current_from_party, to_party=bank)

        

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_C
            self.workflowitems.final_state = StateChoices.STATUS_ACCEPTED
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.subaction = StateChoices.SIGN_B
            self.workflowitems.action = 'ACCEPT'
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, event_user = user , type = "PROGRAM",
                                      to_state=StateChoices.STATUS_ACCEPTED, interim_state=StateChoices.STATUS_AWAITING_SIGN_C, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_C, target=StateChoices.STATUS_ACCEPTED)
    def accept_level_3(self,request):
        user = myuser(request)
        bank = Parties.objects.get(party_type="BANK")
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="ACCEPT", model="PROGRAM")

        if obj.sign_c == True:
            self.workflowitems.interim_state = StateChoices.STATUS_ACCEPTED
            self.workflowitems.final_state = StateChoices.STATUS_ACCEPTED
            self.workflowitems.current_to_party = bank
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action = 'ACCEPT'
            self.workflowitems.subaction = StateChoices.SIGN_C
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_C, final='YES', event_user = user ,type = "PROGRAM",
                                      to_state=StateChoices.STATUS_ACCEPTED, interim_state=StateChoices.STATUS_ACCEPTED, from_party=self.workflowitems.current_from_party, to_party=bank)
        return None
        
# APPROVE TRANSITION

    @stage.transition(source=StateChoices.STATUS_AW_APPROVAL, target=StateChoices.STATUS_AWAITING_SIGN_A)
    def approve(self):
        user = myuser(request)
        party = request.user.party
        bank = Parties.objects.get(party_type="BANK")
        obj = signatures.objects.get(
            party=bank, action__desc__contains="APPROVE", model="PROGRAM")

        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A]
            self.workflowitems.current_to_party = self.workflowitems.current_from_party = party
            self.workflowitems.action = 'APPROVE'
            self.workflowitems.subaction = StateChoices.MAKER
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_APPROVAL, to_state=StateChoices.STATUS_APPROVED, event_user = user , type = "PROGRAM",
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]
            self.workflowitems.current_to_party = self.workflowitems.current_from_party = party
            self.workflowitems.action = 'APPROVE'
            self.workflowitems.subaction = StateChoices.MAKER
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_APPROVAL, to_state=StateChoices.STATUS_APPROVED, event_user = user, type = "PROGRAM",
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED
            self.workflowitems.current_to_party = self.workflowitems.current_from_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.action = 'APPROVE'
            self.workflowitems.subaction = StateChoices.MAKER
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_APPROVAL, to_state=StateChoices.STATUS_APPROVED, event_user = user ,type = "PROGRAM",
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_A, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def approve_signA(self):
        user = myuser(request)
        party = request.user.party
        bank = Parties.objects.get(party_type="BANK")
        obj = signatures.objects.get(
            party=bank, action__desc__contains="APPROVE", model="PROGRAM")

        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):

            self.workflowitems.interim_state = StateChoices.STATUS_APPROVED
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED
            self.workflowitems.current_from_party , self.workflowitems.current_to_party = bank , self.workflowitems.user.party
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action = 'APPROVE'
            self.workflowitems.subaction = StateChoices.MAKER
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_APPROVED, event_user = user , type = "PROGRAM",
                                      interim_state=StateChoices.STATUS_APPROVED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, c_final="YES")

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED
            self.workflowitems.current_to_party = self.workflowitems.current_from_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B]
            self.workflowitems.action = 'APPROVE'
            self.workflowitems.subaction = StateChoices.MAKER
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_APPROVED, event_user = user ,type = "PROGRAM",
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED
            self.workflowitems.current_to_party = self.workflowitems.current_from_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.action = 'APPROVE'
            self.workflowitems.subaction = StateChoices.MAKER
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_APPROVED, event_user = user , type = "PROGRAM",
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_B, target=StateChoices.STATUS_AWAITING_SIGN_C)
    def approve_signB(self):
        user = myuser(request)
        bank = Parties.objects.get(party_type="BANK")
        obj = signatures.objects.get(
            party=bank, action__desc__contains="APPROVE", model="PROGRAM")

        if (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):

            self.workflowitems.interim_state = StateChoices.STATUS_APPROVED
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.current_from_party , self.workflowitems.current_to_party = bank , self.workflowitems.user.party
            self.workflowitems.action = 'APPROVE'
            self.workflowitems.subaction = StateChoices.MAKER
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, to_state=StateChoices.STATUS_APPROVED, event_user = user ,type = "PROGRAM",
                                      interim_state=StateChoices.STATUS_APPROVED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, c_final='YES')

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_C
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.action = 'APPROVE'
            self.workflowitems.subaction = StateChoices.MAKER
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, to_state=StateChoices.STATUS_APPROVED, event_user = user , type = "PROGRAM",
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_C, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

                                      
    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_C, target=StateChoices.STATUS_APPROVED)
    def approve_signC(self):
        user = myuser(request) 
        bank = Parties.objects.get(party_type="BANK")
        obj = signatures.objects.get(
            party=bank, action__desc__contains="APPROVE", model="PROGRAM")

        if (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):

            self.workflowitems.interim_state = StateChoices.STATUS_APPROVED
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED
            self.workflowitems.current_from_party , self.workflowitems.current_to_party = bank , self.workflowitems.user.party
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action = 'APPROVE'
            self.workflowitems.subaction = StateChoices.MAKER
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_C, to_state=StateChoices.STATUS_APPROVED, event_user = user ,type = "PROGRAM",
                                      interim_state=StateChoices.STATUS_APPROVED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, c_final='YES')
                                      

    
# --------------------------------------------------------------------------------------------------
# DELETE TRANSITION
# --------------------------------------------------------------------------------------------------

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_DELETED)
    def delete(self):
        user = self.workflowitems.event_users
        self.workflowitems.interim_state = StateChoices.STATUS_DELETED
        self.workflowitems.final_state = StateChoices.STATUS_DELETED
        self.workflowitems.current_from_party = self.workflowitems.current_to_party = self.workflowitems.user.party
        self.workflowitems.action = 'DELETE'
        ws = workflowitems.objects.get(id=self.workflowitems.id)
        workevents.objects.create(workitems=ws, from_state='STATUS_DELETED', to_state='STATUS_DELETED', event_user = user , type = "PROGRAM",
                                  interim_state='STATUS_DELETED', from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party,c_final = "YES")


# --------------------------------------------------------------------------------------------------
# RETURN TRANSITION
# --------------------------------------------------------------------------------------------------

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_DRAFT)
    def returns(self,request):
        bank = Parties.objects.get(party_type="BANK")
        user = self.workflowitems.event_users
        self.workflowitems.interim_state = StateChoices.STATUS_DRAFT
        self.workflowitems.final_state = StateChoices.STATUS_DRAFT
        self.workflowitems.current_from_party = self.workflowitems.current_to_party = self.workflowitems.user.party
        self.workflowitems.action = 'RETURN'
        ws = workflowitems.objects.get(id=self.workflowitems.id)
        cs = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_ACCEPT, to_state=StateChoices.STATUS_DRAFT, event_user = user , 
                                  interim_state=StateChoices.STATUS_DRAFT, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)
    
        # if request.user.is_administrator == True:
        #     cs.c_final = "YES"
        #     cs.to_party = bank
        #     cs.save()
        # else:
        #     cs.final = "YES"
        #     cs.save()
