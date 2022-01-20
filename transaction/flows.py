
from sre_parse import State
from transaction.states import StateChoices
from transaction.models import workevents, workflowitems
from viewflow import fsm


class WorkFlow(object):
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

    #  <> ----------------- ACTION : SUBMIT --------------------- <>

    @stage.transition(source=StateChoices.STATUS_DRAFT, target=StateChoices.STATUS_AWAITING_SIGN_A)
    def submit(self):
        # self.workflowitems.initial_state = StateChoices.STATUS_DRAFT
        self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
        self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL
        self.workflowitems.action = 'SUBMIT'
        ws = workflowitems.objects.get(id=self.workflowitems.id)
        workevents.objects.create(workitems=ws, from_state='DRAFT', to_state='AWAITING_APPROVAL',
                                  interim_state='AWAITING_SIGN_A', from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_A, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def submit_level_1(self):
        # self.workflowitems.initial_state = StateChoices.STATUS_AWAITING_SIGN_A
        self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
        self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL
        self.workflowitems.action = 'SUBMIT'
        ws = workflowitems.objects.get(id=self.workflowitems.id)
        workevents.objects.create(workitems=ws, from_state='AWAITING_SIGN_A',
                                  to_state='AWAITING_APPROVAL', interim_state='AWAITING_SIGN_B', from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_B, target=StateChoices.STATUS_AWAITING_SIGN_C)
    def submit_level_2(self):
        self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_C
        self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL
        self.workflowitems.action = 'SUBMIT'
        ws = workflowitems.objects.get(id=self.workflowitems.id)
        workevents.objects.create(workitems=ws, from_state='AWAITING_SIGN_B',
                                  to_state='AWAITING_APPROVAL', interim_state='AWAITING_SIGN_C', from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_C, target=StateChoices.STATUS_AW_APPROVAL)
    def submit_level_3(self):
        self.workflowitems.interim_state = StateChoices.STATUS_AW_APPROVAL
        self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL
        self.workflowitems.initial_state = StateChoices.STATUS_AW_ACCEPT
        self.workflowitems.action = 'SUBMIT'
        ws = workflowitems.objects.get(id=self.workflowitems.id)
        workevents.objects.create(workitems=ws, from_state='AWAITING_SIGN_C',
                                  to_state='AWAITING_APPROVAL', interim_state='AWAITING_APPROVAL', from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    #  <> ----------------- ACTION : REJECT --------------------- <>

    @stage.transition(source=StateChoices.STATUS_AW_ACCEPT, target=StateChoices.STATUS_AWAITING_SIGN_A)
    def reject(self):
        self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
        self.workflowitems.final_state = StateChoices.STATUS_REJECTED
        self.workflowitems.action = "REJECT"
        ws = workflowitems.objects.get(id=self.workflowitems.id)
        workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_ACCEPT,
                                  to_state=StateChoices.STATUS_REJECTED, interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_A, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def reject_level_1(self):
        self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
        self.workflowitems.final_state = StateChoices.STATUS_REJECTED
        self.workflowitems.action = "REJECT"
        ws = workflowitems.objects.get(id=self.workflowitems.id)
        workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A,
                                  to_state=StateChoices.STATUS_REJECTED, interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_B, target=StateChoices.STATUS_AWAITING_SIGN_C)
    def reject_level_2(self):
        self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_C
        self.workflowitems.final_state = StateChoices.STATUS_REJECTED
        self.workflowitems.action = "REJECT"
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

    #  <> ----------------- ACTION : ACCEPT --------------------- <>

    @stage.transition(source=StateChoices.STATUS_AW_ACCEPT, target=StateChoices.STATUS_AWAITING_SIGN_A)
    def accept(self):
        self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
        self.workflowitems.final_state = StateChoices.STATUS_ACCEPTED
        self.workflowitems.action = 'ACCEPT'
        ws = workflowitems.objects.get(id=self.workflowitems.id)
        workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AW_ACCEPT,
                                  to_state=StateChoices.STATUS_ACCEPTED, interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_A, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def accept_level_1(self):
        self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
        self.workflowitems.final_state = StateChoices.STATUS_ACCEPTED
        self.workflowitems.action = 'ACCEPT'
        ws = workflowitems.objects.get(id=self.workflowitems.id)
        workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A,
                                  to_state=StateChoices.STATUS_ACCEPTED, interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_B, target=StateChoices.STATUS_AWAITING_SIGN_C)
    def accept_level_2(self):
        self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_C
        self.workflowitems.final_state = StateChoices.STATUS_ACCEPTED
        self.workflowitems.action = 'ACCEPT'
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
