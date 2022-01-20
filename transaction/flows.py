
from transaction.states import StateChoices
from transaction.models import workflowitems
from viewflow import fsm


class WorkFlow(object):
    workitems = workflowitems()
    stage = fsm.State(StateChoices, default=StateChoices.STATUS_DRAFT)

    def __init__(self, status):
        self.status = status

    @stage.setter()
    def _set_status_stage(self, value):
        self.status.stage = value

    @stage.getter()
    def _get_status(self):
        return self.status.stage

    @stage.transition(source=StateChoices.STATUS_DRAFT, target=StateChoices.STATUS_AWAITING_SIGN_A)
    def submit(self):
        self.workitems.initial_state = StateChoices.STATUS_DRAFT
        self.workitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
        self.workitems.final_state = StateChoices.STATUS_AW_APPROVAL

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_A, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def submit_level_1(self):
        self.workitems.initial_state = StateChoices.STATUS_AWAITING_SIGN_A
        self.workitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
        self.workitems.final_state = StateChoices.STATUS_AW_APPROVAL
