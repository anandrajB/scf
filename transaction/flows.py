
from transaction.states import StateChoices
from transaction.models import workflowitems
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

    @stage.transition(source=StateChoices.STATUS_DRAFT, target=StateChoices.STATUS_AWAITING_SIGN_A)
    def submit(self):
        self.workflowitems.initial_state = StateChoices.STATUS_DRAFT
        self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
        self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_A, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def submit_level_1(self):
        self.workflowitems.initial_state = StateChoices.STATUS_AWAITING_SIGN_A
        self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
        self.workflowitems.final_state = StateChoices.STATUS_AW_APPROVAL
