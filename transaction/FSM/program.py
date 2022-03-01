# django fsm flows using djano-viewflow package == 2.0a02
from urllib import request
from transaction.states import StateChoices
from transaction.models import workevents, workflowitems
from viewflow import fsm
from accounts.models import Parties ,  signatures
from transaction.views import  currentuser, myfun


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
        bank = Parties.objects.get(party_type="BANK")
        user = self.workflowitems.event_users
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="SUBMIT", model="PROGRAM")

        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.initial_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A]
            self.workflowitems.action = 'SUBMIT'
            self.workflowitems.subaction = StateChoices.SUBMIT
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_AW_APPROVAL,user =  user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=bank)

        

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.initial_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]
            self.workflowitems.action = 'SUBMIT'
            self.workflowitems.subaction = StateChoices.SUBMIT
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_AW_APPROVAL, user = user ,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=bank)

       

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.action = 'SUBMIT'
            self.workflowitems.subaction = StateChoices.SUBMIT
            self.workflowitems.initial_state = StateChoices.STATUS_AWAITING_SIGN_A
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_AW_APPROVAL, user = user ,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=bank)

    
        

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_A, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def submit_level_1(self,request):
        user = self.workflowitems.event_users
        bank = Parties.objects.get(party_type="BANK")
        obj = signatures.objects.get(
             action__desc__contains="SUBMIT", model="PROGRAM")

        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action = 'SUBMIT'
            self.workflowitems.subaction = StateChoices.SIGN_A
            self.workflowitems.initial_state = StateChoices.STATUS_AW_ACCEPT
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            cs = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, user = user , 
                                      to_state=StateChoices.STATUS_AW_APPROVAL, interim_state=StateChoices.STATUS_AW_APPROVAL, from_party=self.workflowitems.current_from_party, to_party=bank)
            if request.user.is_administrator == True:
                cs.c_final = "YES"
                cs.save()
            else:
                cs.final = "YES"
                cs.save()
        # elif (obj.sign_a != True and obj.sign_b == True and obj.sign_c != True):
        #     pass

        # elif (obj.sign_a != True and obj.sign_b != True and obj.sign_c == True):
        #     pass

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.action = 'SUBMIT'
            self.workflowitems.initial_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.subaction = StateChoices.SIGN_A
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B]
            # self.workflowitems.initial_state = StateChoices.STATUS_AW_ACCEPT
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, user = user , 
                                      to_state=StateChoices.STATUS_AW_APPROVAL, interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        

        # elif (obj.sign_a != True and obj.sign_b == True and obj.sign_c == True):
        #     pass

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.initial_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.subaction = StateChoices.SIGN_A
            self.workflowitems.action = 'SUBMIT'
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, user = user , 
                                      to_state=StateChoices.STATUS_AW_APPROVAL, interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_B, target=StateChoices.STATUS_AWAITING_SIGN_C)
    def submit_level_2(self,request):
        user = self.workflowitems.event_users
        bank = Parties.objects.get(party_type="BANK")
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="SUBMIT", model="PROGRAM")

        # elif (obj.sign_a != True and obj.sign_b != True and obj.sign_c == True):
        #     pass

        if (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.next_available_transitions = []
            self.workflowitems.subaction = StateChoices.SIGN_B
            self.workflowitems.action = 'SUBMIT'
            self.workflowitems.initial_state = StateChoices.STATUS_AW_ACCEPT
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            cs = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, user = user , 
                                      to_state=StateChoices.STATUS_AW_APPROVAL, interim_state=StateChoices.STATUS_AW_APPROVAL, from_party=self.workflowitems.current_from_party, to_party=bank)
            if request.user.is_administrator == True:
                cs.c_final = "YES"
                cs.save()
            else:
                cs.final = "YES"
                cs.save()

       

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_C
            self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.subaction = StateChoices.SIGN_B
            self.workflowitems.action = 'SUBMIT'
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, user = user , 
                                      to_state=StateChoices.STATUS_AW_APPROVAL, interim_state=StateChoices.STATUS_AWAITING_SIGN_C, from_party=self.workflowitems.current_from_party, to_party=bank)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_C, target=StateChoices.STATUS_AW_APPROVAL)
    def submit_level_3(self,request):
        bank = Parties.objects.get(party_type="BANK")
        user = self.workflowitems.event_users
        self.workflowitems.interim_state = StateChoices.STATUS_AW_APPROVAL
        self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL
        self.workflowitems.initial_state = StateChoices.STATUS_AW_ACCEPT
        self.workflowitems.next_available_transitions = []
        self.workflowitems.action = 'SUBMIT'
        self.workflowitems.subaction = StateChoices.SIGN_C
        ws = workflowitems.objects.get(id=self.workflowitems.id)
        cs = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_C,  user = user,
                                  to_state=StateChoices.STATUS_AW_APPROVAL, interim_state=StateChoices.STATUS_AW_APPROVAL, from_party=self.workflowitems.current_from_party, to_party=bank)
        if request.user.is_administrator == True:
            cs.c_final = "YES"
            cs.save()
        else:
            cs.final = "YES"
            cs.save()

# -------------------------------------------------------------------------------------------------
# REJECT TRANSITIONS
# --------------------------------------------------------------------------------------------------
    def myfun(request):
        user = request.user
        bank = Parties.objects.get(party_type="BANK")
        if user.is_administrator == True:
            rejects = signatures.objects.get(
                    party=bank, action__desc__contains="REJECT", model="PROGRAM")
            
        else :
            rejects = signatures.objects.get(
                    party=user.party, action__desc__contains="REJECT", model="PROGRAM")
        
        return rejects

    @stage.transition(source=StateChoices.STATUS_AW_ACCEPT, target=StateChoices.STATUS_AWAITING_SIGN_A)
    def reject(self,request):
        user = self.workflowitems.event_users
        bank = Parties.objects.get(party_type="BANK")
        # obj = signatures.objects.get(
        #     party=bank, action__desc__contains="REJECT", model="PROGRAM")
        obj = myfun(request)
        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED
            self.workflowitems.initial_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A]
            self.workflowitems.action = 'REJECT'
            self.workflowitems.subaction = StateChoices.MAKER
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_ACCEPT, to_state=StateChoices.STATUS_REJECTED, user = user , 
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=bank)

       

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED
            self.workflowitems.initial_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]
            self.workflowitems.action = 'REJECT'
            self.workflowitems.subaction = StateChoices.MAKER
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_ACCEPT, to_state=StateChoices.STATUS_REJECTED, user =  user , 
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=bank)

        

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.initial_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.action = 'REJECT'
            self.workflowitems.subaction = StateChoices.MAKER
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_ACCEPT, to_state=StateChoices.STATUS_REJECTED, user = user , 
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=bank)


    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_A, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def reject_level_1(self,request):
        user = self.workflowitems.event_users
        bank = Parties.objects.get(party_type="BANK")
        # obj = signatures.objects.get(
        #     party=bank, action__desc__contains="REJECT", model="PROGRAM")
        obj = myfun(request)
        user = self.workflowitems.event_users
        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_REJECTED
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.subaction = "SIGN_A"
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            
            if request.user.is_administrator == True:
                cs = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, user = user , 
                                      to_state=StateChoices.STATUS_REJECTED, interim_state=StateChoices.STATUS_REJECTED, from_party=self.workflowitems.current_from_party, to_party=bank)
                cs.c_final = "YES"
                cs.save()
            else:
                cs = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, user = user , 
                                      to_state=StateChoices.STATUS_REJECTED, interim_state=StateChoices.STATUS_REJECTED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_from_party)
                cs.final = "YES"
                cs.save()
        # elif (obj.sign_a != True and obj.sign_b == True and obj.sign_c != True):
        #     pass

        # elif (obj.sign_a != True and obj.sign_b != True and obj.sign_c == True):
        #     pass

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED
            self.workflowitems.initial_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B]
            self.workflowitems.action = 'REJECT'
            self.workflowitems.initial_state = StateChoices.STATUS_AW_ACCEPT
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A,user = user , 
                                      to_state=StateChoices.STATUS_REJECTED, interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=bank)

       

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED
            self.workflowitems.initial_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, user = user , 
                                      to_state=StateChoices.STATUS_REJECTED, interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=bank)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_B, target=StateChoices.STATUS_AWAITING_SIGN_C)
    def reject_level_2(self,request):
        user = self.workflowitems.event_users
        bank = Parties.objects.get(party_type="BANK")
        # obj = signatures.objects.get(
        #     party=bank, action__desc__contains="REJECT", model="PROGRAM")
        obj = myfun(request)
        

        if (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_REJECTED
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.subaction = StateChoices.SIGN_B
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            
            if request.user.is_administrator == True:
                cs = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, user = user,
                                      to_state=StateChoices.STATUS_REJECTED, interim_state=StateChoices.STATUS_REJECTED, from_party=self.workflowitems.current_from_party, to_party=bank)
                cs.c_final = "YES"
                cs.save()
            else:
                cs = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, user = user,
                                      to_state=StateChoices.STATUS_REJECTED, interim_state=StateChoices.STATUS_REJECTED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_from_party)
                cs.final = "YES"
                cs.save()

       

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_C
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.subaction = StateChoices.SIGN_B
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, user = user , 
                                      to_state=StateChoices.STATUS_AW_APPROVAL, interim_state=StateChoices.STATUS_AWAITING_SIGN_C, from_party=self.workflowitems.current_from_party, to_party=bank)


    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_C, target=StateChoices.STATUS_REJECTED)
    def reject_level_3(self,request):
        user = self.workflowitems.event_users
        bank = Parties.objects.get(party_type="BANK")
        obj = myfun(request)
        # obj = signatures.objects.get(
        #     party=bank, action__desc__contains="REJECT", model="PROGRAM")
        if obj.sign_c == True:
            self.workflowitems.interim_state = StateChoices.STATUS_REJECTED
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action = 'REJECT'
            self.workflowitems.subaction = StateChoices.SIGN_C
            ws = workflowitems.objects.get(id=self.workflowitems.id)
           

            if request.user.is_administrator == True:
                cs = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_C, user = user , 
                                      to_state=StateChoices.STATUS_AW_APPROVAL, interim_state=StateChoices.STATUS_AW_APPROVAL, from_party=self.workflowitems.current_from_party, to_party=bank)
                cs.c_final = "YES"
                cs.save()
            else:
                cs = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_C, user = user , 
                                      to_state=StateChoices.STATUS_AW_APPROVAL, interim_state=StateChoices.STATUS_AW_APPROVAL, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_from_party)
                cs.final = "YES"
                cs.save()

    
# -------------------------------------------------------------------------------------------------
# ACCEPT TRANSITION
# --------------------------------------------------------------------------------------------------

    @stage.transition(source=StateChoices.STATUS_AW_ACCEPT, target=StateChoices.STATUS_AWAITING_SIGN_A)
    def accept(self,request):
        user = self.workflowitems.event_users
        bank = Parties.objects.get(party_type="BANK")
        obj = signatures.objects.get(
            party=bank, action__desc__contains="ACCEPT", model="PROGRAM")

        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_ACCEPTED
            self.workflowitems.initial_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A]
            self.workflowitems.action = 'ACCEPT'
            self.workflowitems.subaction = StateChoices.MAKER
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_ACCEPT, to_state=StateChoices.STATUS_ACCEPTED, user = user , 
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=bank)

        

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_ACCEPTED
            self.workflowitems.initial_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]
            self.workflowitems.action = 'ACCEPT'
            self.workflowitems.subaction = StateChoices.MAKER
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_ACCEPTED, user = user , 
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=bank)

       

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_ACCEPTED
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.action = 'ACCEPT'
            self.workflowitems.subaction = StateChoices.MAKER
            self.workflowitems.initial_state = StateChoices.STATUS_AWAITING_SIGN_A
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_ACCEPTED, user = user , 
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=bank)


    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_A, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def accept_level_1(self):
        user = self.workflowitems.event_users
        bank = Parties.objects.get(party_type="BANK")
        obj = signatures.objects.get(
            party=bank, action__desc__contains="ACCEPT", model="PROGRAM")

        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_ACCEPTED
            self.workflowitems.final_state = StateChoices.STATUS_ACCEPTED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action = 'ACCEPT'
            self.workflowitems.subaction = StateChoices.SIGN_A
            self.workflowitems.initial_state = StateChoices.STATUS_AW_ACCEPT
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, final='YES', user = user , 
                                      to_state=StateChoices.STATUS_ACCEPTED, interim_state=StateChoices.STATUS_ACCEPTED, from_party=self.workflowitems.current_from_party, to_party=bank)

        # elif (obj.sign_a != True and obj.sign_b == True and obj.sign_c != True):
        #     pass

        # elif (obj.sign_a != True and obj.sign_b != True and obj.sign_c == True):
        #     pass

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
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, user = user , 
                                      to_state=StateChoices.STATUS_ACCEPTED, interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=bank)


        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_ACCEPTED
            self.workflowitems.initial_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.subaction = StateChoices.SIGN_A
            self.workflowitems.action = 'ACCEPT'
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, user = user , 
                                      to_state=StateChoices.STATUS_ACCEPTED, interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=bank)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_B, target=StateChoices.STATUS_AWAITING_SIGN_C)
    def accept_level_2(self):
        user = self.workflowitems.event_users
        bank = Parties.objects.get(party_type="BANK")
        obj = signatures.objects.get(
            party=bank, action__desc__contains="ACCEPT", model="PROGRAM")

       

        if (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_ACCEPTED
            self.workflowitems.final_state = StateChoices.STATUS_ACCEPTED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.subaction = StateChoices.SIGN_B
            self.workflowitems.action = 'ACCEPT'
            self.workflowitems.initial_state = StateChoices.STATUS_AW_ACCEPT
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, final='YES', user = user , 
                                      to_state=StateChoices.STATUS_ACCEPTED, interim_state=StateChoices.STATUS_ACCEPTED, from_party=self.workflowitems.current_from_party, to_party=bank)

        

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_C
            self.workflowitems.final_state = StateChoices.STATUS_ACCEPTED
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.subaction = StateChoices.SIGN_B
            self.workflowitems.action = 'ACCEPT'
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, user = user , 
                                      to_state=StateChoices.STATUS_ACCEPTED, interim_state=StateChoices.STATUS_AWAITING_SIGN_C, from_party=self.workflowitems.current_from_party, to_party=bank)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_C, target=StateChoices.STATUS_ACCEPTED)
    def accept_level_3(self):
        user = self.workflowitems.event_users
        bank = Parties.objects.get(party_type="BANK")
        obj = signatures.objects.get(
            party=bank, action__desc__contains="ACCEPT", model="PROGRAM")

        if obj.sign_c == True:
            self.workflowitems.interim_state = StateChoices.STATUS_ACCEPTED
            self.workflowitems.final_state = StateChoices.STATUS_ACCEPTED
            # self.workflowitems.initial_state = StateChoices.STATUS_AW_ACCEPT
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action = 'ACCEPT'
            self.workflowitems.subaction = StateChoices.SIGN_C
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_C, final='YES', user = user ,
                                      to_state=StateChoices.STATUS_ACCEPTED, interim_state=StateChoices.STATUS_ACCEPTED, from_party=self.workflowitems.current_from_party, to_party=bank)
        return None



# APPROVE TRANSITION

    @stage.transition(source=StateChoices.STATUS_AW_APPROVAL, target=StateChoices.STATUS_AWAITING_SIGN_A)
    def approve(self):
        user = self.workflowitems.event_users
        bank = Parties.objects.get(party_type="BANK")
        obj = signatures.objects.get(
            party=bank, action__desc__contains="APPROVE", model="PROGRAM")

        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A]
            self.workflowitems.action = 'APPROVE'
            self.workflowitems.subaction = StateChoices.MAKER
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_APPROVAL, to_state=StateChoices.STATUS_APPROVED, user = user , 
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=bank)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]
            self.workflowitems.action = 'APPROVE'
            self.workflowitems.subaction = StateChoices.MAKER
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_APPROVAL, to_state=StateChoices.STATUS_APPROVED, user = user, 
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=bank)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.action = 'APPROVE'
            self.workflowitems.subaction = StateChoices.MAKER
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_APPROVAL, to_state=StateChoices.STATUS_APPROVED, user = user ,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=bank)


    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_A, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def approve_signA(self):
        user = self.workflowitems.event_users
        bank = Parties.objects.get(party_type="BANK")
        obj = signatures.objects.get(
            party=bank, action__desc__contains="APPROVE", model="PROGRAM")

        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):

            self.workflowitems.interim_state = StateChoices.STATUS_APPROVED
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action = 'APPROVE'
            self.workflowitems.subaction = StateChoices.MAKER
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_APPROVED, user = user , 
                                      interim_state=StateChoices.STATUS_APPROVED, from_party=self.workflowitems.current_from_party, to_party=bank, c_final="YES")

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B]
            self.workflowitems.action = 'APPROVE'
            self.workflowitems.subaction = StateChoices.MAKER
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_APPROVED, user = user ,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=bank)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.action = 'APPROVE'
            self.workflowitems.subaction = StateChoices.MAKER
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_APPROVED, user = user , 
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=bank)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_B, target=StateChoices.STATUS_AWAITING_SIGN_C)
    def approve_signB(self):
        user = self.workflowitems.event_users
        bank = Parties.objects.get(party_type="BANK")
        obj = signatures.objects.get(
            party=bank, action__desc__contains="APPROVE", model="PROGRAM")

        if (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):

            self.workflowitems.interim_state = StateChoices.STATUS_APPROVED
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action = 'APPROVE'
            self.workflowitems.subaction = StateChoices.MAKER
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, to_state=StateChoices.STATUS_APPROVED, user = user ,
                                      interim_state=StateChoices.STATUS_APPROVED, from_party=self.workflowitems.current_from_party, to_party=bank, c_final='YES')

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_C
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.action = 'APPROVE'
            self.workflowitems.subaction = StateChoices.MAKER
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, to_state=StateChoices.STATUS_APPROVED, user = user , 
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_C, from_party=self.workflowitems.current_from_party, to_party=bank)

                                      
    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_C, target=StateChoices.STATUS_APPROVED)
    def approve_signC(self):
        user = self.workflowitems.event_users 
        bank = Parties.objects.get(party_type="BANK")
        obj = signatures.objects.get(
            party=bank, action__desc__contains="APPROVE", model="PROGRAM")

        if (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):

            self.workflowitems.interim_state = StateChoices.STATUS_APPROVED
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action = 'APPROVE'
            self.workflowitems.subaction = StateChoices.MAKER
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_C, to_state=StateChoices.STATUS_APPROVED, user = user ,
                                      interim_state=StateChoices.STATUS_APPROVED, from_party=self.workflowitems.current_from_party, to_party=bank, c_final='YES')
                                      

    
# --------------------------------------------------------------------------------------------------
# DELETE TRANSITION
# --------------------------------------------------------------------------------------------------

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_DELETED)
    def delete(self):
        user = self.workflowitems.event_users
        self.workflowitems.interim_state = StateChoices.STATUS_DELETED
        self.workflowitems.final_state = StateChoices.STATUS_DELETED
        self.workflowitems.action = 'DELETE'
        ws = workflowitems.objects.get(id=self.workflowitems.id)
        workevents.objects.create(workitems=ws, from_state='STATUS_DELETED', to_state='STATUS_DELETED', user = user , 
                                  interim_state='STATUS_DELETED', from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party,c_final = "YES")


# --------------------------------------------------------------------------------------------------
# RETURN TRANSITION
# --------------------------------------------------------------------------------------------------

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_DRAFT)
    def returns(self,request):

        user = self.workflowitems.event_users
        self.workflowitems.interim_state = StateChoices.STATUS_DRAFT
        self.workflowitems.final_state = StateChoices.STATUS_DRAFT
        self.workflowitems.action = 'RETURN'
        ws = workflowitems.objects.get(id=self.workflowitems.id)
        cs = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_ACCEPT, to_state=StateChoices.STATUS_DRAFT, user = user , 
                                  interim_state=StateChoices.STATUS_DRAFT, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)
    
        if request.user.is_administrator == True:
            cs.c_final = "YES"
            cs.save()
        else:
            cs.final = "YES"
            cs.save()
