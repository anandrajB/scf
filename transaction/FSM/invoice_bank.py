# # django fsm flows using djano-viewflow package == 2.0a02
from transaction.states import StateChoices
from transaction.models import workevents, workflowitems
from viewflow import fsm
from accounts.models import signatures, Parties
from accounts.models import userprocessauth

# Function to get wf_item_id


def gets_wf_item_id(id):
    return workflowitems.objects.get(id=id)


# Function to APPROVE for user type "BANK"

def approve_transition(request):
    user = request.user
    bank = Parties.objects.get(party_type='BANK')
    if user.party.party_type == "BANK":
        qs = signatures.objects.get(
            party=bank, action__desc__contains="APPROVE", model="INVOICE")
    else:
        return None

    return qs

# Function to REJECT for user type "BANK"


def reject_transition(request):
    user = request.user
    bank = Parties.objects.get(party_type='BANK')
    if user.party.party_type == "BANK":
        obj = signatures.objects.get(
            party=bank, action__desc__contains="REJECT", model="INVOICE")

    return obj

# Function to SETTLE for user type "BANK"


def settle_transition(request):
    user = request.user
    bank = Parties.objects.get(party_type='BANK')
    if user.party.party_type == "BANK":
        obj = signatures.objects.get(
            party=bank, action__desc__contains="SETTLE", model="INVOICE")

    return obj

# Function to OVERDUE for user type "BANK"


def overdue_transition(request):
    user = request.user
    bank = Parties.objects.get(party_type='BANK')
    if user.party.party_type == "BANK":
        obj = signatures.objects.get(
            party=bank, action__desc__contains="OVERDUE", model="INVOICE")

    return obj


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


# REJECT TRANSITION

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AWAITING_SIGN_A)
    def reject_invoice(self, request):
        user = request.user
        party = request.user.party
        obj = reject_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REJECTED
            self.workflowitems.action = "REJECT"
            self.workflowitems.current_from_party = self.workflowitems.current_from_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_FINANCE_REQUESTED, to_state=StateChoices.STATUS_FINANCE_REJECTED, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REJECTED
            self.workflowitems.action = "REJECT"
            self.workflowitems.current_from_party = self.workflowitems.current_from_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_FINANCE_REQUESTED, to_state=StateChoices.STATUS_FINANCE_REJECTED, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REJECTED
            self.workflowitems.action = "REJECT"
            self.workflowitems.current_from_party = self.workflowitems.current_from_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_FINANCE_REQUESTED, to_state=StateChoices.STATUS_FINANCE_REJECTED, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def reject_inv_signA(self, request):

        user = request.user
        party = request.user.party
        obj = reject_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_FINANCE_REJECTED
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REJECTED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action = "REJECT"
            self.workflowitems.current_from_party = party
            self.workflowitems.current_to_party = self.workflowitems.user.party

            cc = workevents.objects.create(
                workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, interim_state=StateChoices.STATUS_FINANCE_REJECTED, to_state=StateChoices.STATUS_FINANCE_REJECTED, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "BANK":
                cc.s_final = 'YES'
                cc.to_party = self.workflowitems.user.party
                cc.save()

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REJECTED
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B]
            self.workflowitems.action = "REJECT"
            self.workflowitems.current_from_party = self.workflowitems.current_from_party = party

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, interim_state=StateChoices.STATUS_AWAITING_SIGN_B,
                                      final_state=StateChoices.STATUS_FINANCE_REJECTED, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REJECTED
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.action = "REJECT"
            self.workflowitems.current_from_party = self.workflowitems.current_from_party = party

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, interim_state=StateChoices.STATUS_AWAITING_SIGN_B,
                                      final_state=StateChoices.STATUS_FINANCE_REJECTED, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_B, target=StateChoices.STATUS_AWAITING_SIGN_C)
    def reject_inv_signB(self, request):

        user = request.user
        party = request.user.party
        obj = reject_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_FINANCE_REJECTED
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REJECTED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action = "REJECT"
            self.workflowitems.current_from_party = party
            self.workflowitems.current_to_party = self.workflowitems.user.party

            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, interim_state=StateChoices.STATUS_FINANCE_REJECTED,
                                           final_state=StateChoices.STATUS_FINANCE_REJECTED, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "BANK":
                cc.s_final = 'YES'
                cc.to_party = self.workflowitems.user.party
                cc.save()

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_C
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REJECTED
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.action = "REJECT"
            self.workflowitems.current_from_party = self.workflowitems.current_from_party = party

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, interim_state=StateChoices.STATUS_AWAITING_SIGN_C,
                                      final_state=StateChoices.STATUS_FINANCE_REJECTED, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_C, target=StateChoices.STATUS_SETTLED)
    def reject_inv_signC(self, request):

        user = request.user
        party = request.user.party
        obj = reject_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_FINANCE_REJECTED
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REJECTED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action = "REJECT"
            self.workflowitems.current_from_party = party
            self.workflowitems.current_to_party = self.workflowitems.user.party

            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_C, interim_state=StateChoices.STATUS_FINANCE_REJECTED,
                                           final_state=StateChoices.STATUS_FINANCE_REJECTED, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "BANK":
                cc.s_final = 'YES'
                cc.to_party = self.workflowitems.user.party
                cc.save()

# APPROVE TRANSITION

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AWAITING_SIGN_A)
    def approve_invoice(self, request):
        user = request.user
        party = request.user.party
        obj = approve_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_FINANCED
            self.workflowitems.action = "APPROVE"
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_FINANCE_REQUESTED, to_state=StateChoices.STATUS_FINANCED, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_FINANCED
            self.workflowitems.action = "APPROVE"
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_FINANCE_REQUESTED, to_state=StateChoices.STATUS_FINANCED, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_FINANCED
            self.workflowitems.action = "APPROVE"
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_FINANCE_REQUESTED, to_state=StateChoices.STATUS_FINANCED, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def approve_inv_signA(self, request):

        user = request.user
        party = request.user.party
        obj = approve_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_FINANCED
            self.workflowitems.final_state = StateChoices.STATUS_FINANCED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action = "APPROVE"
            self.workflowitems.current_from_party = party
            self.workflowitems.current_to_party = self.workflowitems.user.party

            cc = workevents.objects.create(
                workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, interim_state=StateChoices.STATUS_FINANCED, to_state=StateChoices.STATUS_FINANCED, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "BANK":
                cc.s_final = 'YES'
                cc.to_party = self.workflowitems.user.party
                cc.save()

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_FINANCED
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B]
            self.workflowitems.action = "APPROVE"
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, interim_state=StateChoices.STATUS_AWAITING_SIGN_B,
                                      to_state=StateChoices.STATUS_FINANCED, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_FINANCED
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.action = "APPROVE"
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, interim_state=StateChoices.STATUS_AWAITING_SIGN_B,
                                      to_state=StateChoices.STATUS_FINANCED, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AWAITING_SIGN_C)
    def approve_inv_signB(self, request):

        user = request.user
        party = request.user.party
        obj = approve_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_FINANCED
            self.workflowitems.final_state = StateChoices.STATUS_FINANCED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action = "APPROVE"
            self.workflowitems.current_from_party = party
            self.workflowitems.current_to_party = self.workflowitems.user.party

            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, interim_state=StateChoices.STATUS_FINANCED,
                                           to_state=StateChoices.STATUS_FINANCED, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "BANK":
                cc.s_final = 'YES'
                cc.to_party = self.workflowitems.user.party
                cc.save()

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_C
            self.workflowitems.final_state = StateChoices.STATUS_FINANCED
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.action = "APPROVE"
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, interim_state=StateChoices.STATUS_AWAITING_SIGN_C,
                                      to_state=StateChoices.STATUS_FINANCED, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_SETTLED)
    def approve_inv_signC(self, request):

        user = request.user
        party = request.user.party
        obj = approve_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_FINANCED
            self.workflowitems.final_state = StateChoices.STATUS_FINANCED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action = "APPROVE"
            self.workflowitems.current_from_party = party
            self.workflowitems.current_to_party = self.workflowitems.user.party

            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_C, interim_state=StateChoices.STATUS_STATUS_FINANCEDINANCE_REJECTED,
                                           to_state=StateChoices.STATUS_FINANCED, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "BANK":
                cc.s_final = 'YES'
                cc.to_party = self.workflowitems.user.party
                cc.save()

# SETTLE TRANSITION

    @stage.transition(source=StateChoices.STATUS_FINANCED, target=StateChoices.STATUS_SETTLED)
    def settle_invoice(self, request):
        user = request.user
        party = request.user.party
        obj = settle_transition(request)
        ws = workflowitems.objects.get(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):

            self.workflowitems.interim_state = StateChoices.STATUS_SETTLED
            self.workflowitems.final_state = StateChoices.STATUS_SETTLED
            self.workflowitems.action = "SETTLE"
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_FINANCED, to_state=StateChoices.STATUS_SETTLED, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_SETTLED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):

            self.workflowitems.interim_state = StateChoices.STATUS_SETTLED
            self.workflowitems.final_state = StateChoices.STATUS_SETTLED
            self.workflowitems.action = "SETTLE"
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_FINANCED, to_state=StateChoices.STATUS_SETTLED, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_SETTLED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):

            self.workflowitems.interim_state = StateChoices.STATUS_SETTLED
            self.workflowitems.final_state = StateChoices.STATUS_SETTLED
            self.workflowitems.action = "SETTLE"
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_FINANCED, to_state=StateChoices.STATUS_SETTLED, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_SETTLED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_A, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def settle_signA(self, request):

        user = request.user
        party = request.user.party
        obj = settle_transition(request)
        ws = workflowitems.objects.get(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_FINANCE_REJECTED
            self.workflowitems.final_state = StateChoices.STATUS_SETTLED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action = "SETTLE"
            self.workflowitems.current_from_party = party
            self.workflowitems.current_to_party = self.workflowitems.user.party

            cc = workevents.objects.create(
                workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, interim_state=StateChoices.STATUS_SETTLED, to_state=StateChoices.STATUS_SETTLED, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "BANK":
                cc.s_final = 'YES'
                cc.to_party = self.workflowitems.user.party
                cc.save()

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_SETTLED
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B]
            self.workflowitems.action = "SETTLE"
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, interim_state=StateChoices.STATUS_AWAITING_SIGN_B,
                                      final_state=StateChoices.STATUS_SETTLED, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_SETTLED
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.action = "SETTLE"
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, interim_state=StateChoices.STATUS_AWAITING_SIGN_B,
                                      final_state=StateChoices.STATUS_SETTLED, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_B, target=StateChoices.STATUS_AWAITING_SIGN_C)
    def settle_signB(self, request):

        user = request.user
        party = request.user.party
        obj = settle_transition(request)
        ws = workflowitems.objects.get(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_SETTLED
            self.workflowitems.final_state = StateChoices.STATUS_SETTLED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action = "SETTLE"
            self.workflowitems.current_from_party = party
            self.workflowitems.current_to_party = self.workflowitems.user.party

            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, interim_state=StateChoices.STATUS_SETTLED,
                                           final_state=StateChoices.STATUS_SETTLED, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "BANK":
                cc.s_final = 'YES'
                cc.to_party = self.workflowitems.user.party
                cc.save()

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_C
            self.workflowitems.final_state = StateChoices.STATUS_SETTLED
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.action = "SETTLE"
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, interim_state=StateChoices.STATUS_AWAITING_SIGN_C,
                                      final_state=StateChoices.STATUS_SETTLED, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_C, target=StateChoices.STATUS_SETTLED)
    def settle_signC(self, request):

        user = request.user
        party = request.user.party
        obj = settle_transition(request)
        ws = workflowitems.objects.get(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_SETTLED
            self.workflowitems.final_state = StateChoices.STATUS_SETTLED
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action = "SETTLE"
            self.workflowitems.current_from_party = party
            self.workflowitems.current_to_party = self.workflowitems.user.party

            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_C, interim_state=StateChoices.STATUS_SETTLED,
                                           final_state=StateChoices.STATUS_SETTLED, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "BANK":
                cc.s_final = 'YES'
                cc.to_party = self.workflowitems.user.party
                cc.save()

# OVERDUE TRANSITION

    @stage.transition(source=StateChoices.STATUS_FINANCED, target=StateChoices.STATUS_OVERDUE)
    def overdue_invoice(self, request):
        user = request.user
        party = request.user.party
        obj = overdue_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):

            self.workflowitems.interim_state = StateChoices.STATUS_OVERDUE
            self.workflowitems.final_state = StateChoices.STATUS_OVERDUE
            self.workflowitems.action = "OVERDUE"
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_FINANCED, to_state=StateChoices.STATUS_OVERDUE, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_OVERDUE, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):

            self.workflowitems.interim_state = StateChoices.STATUS_OVERDUE
            self.workflowitems.final_state = StateChoices.STATUS_OVERDUE
            self.workflowitems.action = "OVERDUE"
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_FINANCED, to_state=StateChoices.STATUS_OVERDUE, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_OVERDUE, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):

            self.workflowitems.interim_state = StateChoices.STATUS_OVERDUE
            self.workflowitems.final_state = StateChoices.STATUS_OVERDUE
            self.workflowitems.action = "OVERDUE"
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_FINANCED, to_state=StateChoices.STATUS_OVERDUE, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_OVERDUE, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_A, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def overdue_signA(self, request):

        user = request.user
        party = request.user.party
        obj = overdue_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_FINANCE_REJECTED
            self.workflowitems.final_state = StateChoices.STATUS_OVERDUE
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action = "OVERDUE"
            self.workflowitems.current_from_party = party
            self.workflowitems.current_to_party = self.workflowitems.user.party

            cc = workevents.objects.create(
                workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, interim_state=StateChoices.STATUS_FINANCE_REJECTED, to_state=StateChoices.STATUS_OVERDUE, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "BANK":
                cc.s_final = 'YES'
                cc.to_party = self.workflowitems.user.party
                cc.save()

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_OVERDUE
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B]
            self.workflowitems.action = "OVERDUE"
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, interim_state=StateChoices.STATUS_AWAITING_SIGN_B,
                                      final_state=StateChoices.STATUS_OVERDUE, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_OVERDUE
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.action = "SETTLE"
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, interim_state=StateChoices.STATUS_AWAITING_SIGN_B,
                                      final_state=StateChoices.STATUS_SETTLED, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_B, target=StateChoices.STATUS_AWAITING_SIGN_C)
    def overdue_signB(self, request):

        user = request.user
        party = request.user.party
        obj = overdue_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_FINANCE_REJECTED
            self.workflowitems.final_state = StateChoices.STATUS_OVERDUE
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action = "OVERDUE"
            self.workflowitems.current_from_party = party
            self.workflowitems.current_to_party = self.workflowitems.user.party

            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, interim_state=StateChoices.STATUS_FINANCE_REJECTED,
                                           final_state=StateChoices.STATUS_OVERDUE, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "BANK":
                cc.s_final = 'YES'
                cc.to_party = self.workflowitems.user.party
                cc.save()

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_C
            self.workflowitems.final_state = StateChoices.STATUS_OVERDUE
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_C]
            self.workflowitems.action = "OVERDUE"
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, interim_state=StateChoices.STATUS_AWAITING_SIGN_C,
                                      final_state=StateChoices.STATUS_OVERDUE, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_C, target=StateChoices.STATUS_OVERDUE)
    def overdue_signC(self, request):

        user = request.user
        party = request.user.party
        obj = overdue_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_FINANCE_REJECTED
            self.workflowitems.final_state = StateChoices.STATUS_OVERDUE
            self.workflowitems.next_available_transitions = []
            self.workflowitems.action = "OVERDUE"
            self.workflowitems.current_from_party = party
            self.workflowitems.current_to_party = self.workflowitems.user.party

            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_C, interim_state=StateChoices.STATUS_FINANCE_REJECTED,
                                           final_state=StateChoices.STATUS_OVERDUE, type="INVOICE", event_user=user, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "BANK":
                cc.s_final = 'YES'
                cc.to_party = self.workflowitems.user.party
                cc.save()
