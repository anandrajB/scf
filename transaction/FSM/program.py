# django fsm flows using djano-viewflow package == 2.0a02
from transaction.states import StateChoices
from transaction.models import workevents, workflowitems
from viewflow import fsm
from accounts.models import signatures


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

    @stage.transition(source=StateChoices.STATUS_DRAFT, target=StateChoices.STATUS_AWAITING_SIGN_A)
    def submit(self):
        user = self.request.user
        obj = signatures.objects.get(
            party=user.party, action="SUBMIT", model="PROGRAM")
        self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
        self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL

        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A]

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]

        self.workflowitems.action = 'SUBMIT'
        ws = workflowitems.objects.get(id=self.workflowitems.id)
        workevents.objects.create(workitems=ws, from_state='DRAFT', to_state='AWAITING_APPROVAL',
                                  interim_state='AWAITING_SIGN_A', from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_A, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def submit_level_1(self):
        user = self.request.user
        obj = signatures.objects.get(
            party=user.party, action="SUBMIT", model="PROGRAM")

        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.next_available_transitions = []
            self.workflowitems.initial_state = StateChoices.STATUS_AW_ACCEPT
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A,
                                      to_state=StateChoices.STATUS_AW_APPROVAL, interim_state=StateChoices.STATUS_AW_APPROVAL, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B]
            self.workflowitems.initial_state = StateChoices.STATUS_AW_ACCEPT
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A,
                                      to_state=StateChoices.STATUS_AW_APPROVAL, interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A,
                                      to_state=StateChoices.STATUS_AW_APPROVAL, interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_B, target=StateChoices.STATUS_AWAITING_SIGN_C)
    def submit_level_2(self):
        user = self.request.user
        obj = signatures.objects.get(
            party=user.party, action="SUBMIT", model="PROGRAM")

        if (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.next_available_transitions = []
            self.workflowitems.initial_state = StateChoices.STATUS_AW_ACCEPT
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B,
                                      to_state=StateChoices.STATUS_AW_APPROVAL, interim_state=StateChoices.STATUS_AW_APPROVAL, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_C
            self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_C]
            # self.workflowitems.action = 'SUBMIT'
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B,
                                      to_state=StateChoices.STATUS_AW_APPROVAL, interim_state=StateChoices.STATUS_AWAITING_SIGN_C, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_C, target=StateChoices.STATUS_AW_APPROVAL)
    def submit_level_3(self):
        self.workflowitems.interim_state = StateChoices.STATUS_AW_APPROVAL
        self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL
        self.workflowitems.initial_state = StateChoices.STATUS_AW_ACCEPT
        self.workflowitems.action = 'SUBMIT'
        ws = workflowitems.objects.get(id=self.workflowitems.id)
        workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_C,
                                  to_state=StateChoices.STATUS_AW_APPROVAL, interim_state=StateChoices.STATUS_AW_APPROVAL, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

# -------------------------------------------------------------------------------------------------
# REJECT TRANSITIONS
# --------------------------------------------------------------------------------------------------

    @stage.transition(source=StateChoices.STATUS_AW_ACCEPT, target=StateChoices.STATUS_AWAITING_SIGN_A)
    def reject(self):
        user = self.request.user
        obj = signatures.objects.get(
            party=user.party, action="REJECT", model="PROGRAM")

        self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
        self.workflowitems.final_state = StateChoices.STATUS_REJECTED

        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A]

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]

        self.workflowitems.action = "REJECT"
        ws = workflowitems.objects.get(id=self.workflowitems.id)
        workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_ACCEPT,
                                  to_state=StateChoices.STATUS_REJECTED, interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_A, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def reject_level_1(self):
        user = self.request.user
        obj = signatures.objects.get(
            party=user.party, action="REJECT", model="PROGRAM")

        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_REJECTED
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.initial_state = StateChoices.STATUS_AW_ACCEPT
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A,
                                      to_state=StateChoices.STATUS_REJECTED, interim_state=StateChoices.STATUS_REJECTED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A,
                                      to_state=StateChoices.STATUS_REJECTED, interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A,
                                      to_state=StateChoices.STATUS_REJECTED, interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_B, target=StateChoices.STATUS_AWAITING_SIGN_C)
    def reject_level_2(self):
        user = self.request.user
        obj = signatures.objects.get(
            party=user.party, action="REJECT", model="PROGRAM")

        if (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_REJECTED
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.initial_state = StateChoices.STATUS_AW_ACCEPT
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B,
                                      to_state=StateChoices.STATUS_REJECTED, interim_state=StateChoices.STATUS_REJECTED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_C
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED
            # self.workflowitems.action = "REJECT"
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B,
                                      to_state=StateChoices.STATUS_REJECTED, interim_state=StateChoices.STATUS_AWAITING_SIGN_C, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_C, target=StateChoices.STATUS_REJECTED)
    def reject_level_3(self):
        self.workflowitems.interim_state = StateChoices.STATUS_REJECTED
        self.workflowitems.final_state = StateChoices.STATUS_REJECTED
        self.workflowitems.initial_state = StateChoices.STATUS_AW_ACCEPT
        self.workflowitems.action = "REJECT"
        ws = workflowitems.objects.get(id=self.workflowitems.id)
        workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_C,
                                  to_state=StateChoices.STATUS_REJECTED, interim_state=StateChoices.STATUS_REJECTED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)


# -------------------------------------------------------------------------------------------------
# ACCEPT TRANSITION
# --------------------------------------------------------------------------------------------------


    @stage.transition(source=StateChoices.STATUS_AW_ACCEPT, target=StateChoices.STATUS_AWAITING_SIGN_A)
    def accept(self):
        user = self.request.user
        obj = signatures.objects.get(
            party=user.party, action="ACCEPT", model="PROGRAM")
        self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
        self.workflowitems.final_state = StateChoices.STATUS_ACCEPTED

        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A]

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]

        self.workflowitems.action = 'ACCEPT'
        ws = workflowitems.objects.get(id=self.workflowitems.id)
        workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_ACCEPT,
                                  to_state=StateChoices.STATUS_ACCEPTED, interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_A, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def accept_level_1(self):
        user = self.request.user
        obj = signatures.objects.get(
            party=user.party, action="ACCEPT", model="PROGRAM")

        if (obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_ACCEPTED
            self.workflowitems.final_state = StateChoices.STATUS_ACCEPTED
            self.workflowitems.next_available_transitions = []
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A,
                                      to_state=StateChoices.STATUS_ACCEPTED, interim_state=StateChoices.STATUS_ACCEPTED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_ACCEPTED
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A,
                                      to_state=StateChoices.STATUS_ACCEPTED, interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_ACCEPTED
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            # self.workflowitems.action = 'ACCEPT'
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A,
                                      to_state=StateChoices.STATUS_ACCEPTED, interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_B, target=StateChoices.STATUS_AWAITING_SIGN_C)
    def accept_level_2(self):
        user = self.request.user
        obj = signatures.objects.get(
            party=user.party, action="ACTION", model="PROGRAM")

        if (obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_ACCEPTED
            self.workflowitems.final_state = StateChoices.STATUS_ACCEPTED
            self.workflowitems.next_available_transitions = []
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B,
                                      to_state=StateChoices.STATUS_ACCEPTED, interim_state=StateChoices.STATUS_ACCEPTED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif (obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_C
            self.workflowitems.final_state = StateChoices.STATUS_ACCEPTED
            # self.workflowitems.action = 'ACCEPT'
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B,
                                      to_state=StateChoices.STATUS_ACCEPTED, interim_state=StateChoices.STATUS_AWAITING_SIGN_C, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_C, target=StateChoices.STATUS_ACCEPTED)
    def accept_level_3(self):
        self.workflowitems.interim_state = StateChoices.STATUS_ACCEPTED
        self.workflowitems.final_state = StateChoices.STATUS_ACCEPTED
        self.workflowitems.action = 'ACCEPT'
        ws = workflowitems.objects.get(id=self.workflowitems.id)
        workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_C,
                                  to_state=StateChoices.STATUS_ACCEPTED, interim_state=StateChoices.STATUS_ACCEPTED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

# --------------------------------------------------------------------------------------------------
# DELETE TRANSITION
# --------------------------------------------------------------------------------------------------

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_DELETED)
    def delete(self):
        self.workflowitems.interim_state = StateChoices.STATUS_DELETED
        self.workflowitems.final_state = StateChoices.STATUS_DELETED
        self.workflowitems.action = 'DELETE'
        ws = workflowitems.objects.get(id=self.workflowitems.id)
        workevents.objects.create(workitems=ws, from_state='STATUS_DELETED', to_state='STATUS_DELETED',
                                  interim_state='STATUS_DELETED', from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)