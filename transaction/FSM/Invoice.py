# # django fsm flows using djano-viewflow package == 2.0a02
from transaction.states import StateChoices
from transaction.models import workevents, workflowitems
from viewflow import fsm
from accounts.models import signatures, Parties

# Function to get wf_item_id


def gets_wf_item_id(id):
    return workflowitems.objects.get(id=id)


# Function to APPROVE for user type "BUYER"

def approve_transition(request):
    user = request.user
    if user.party.party_type == "BUYER":
        qs = signatures.objects.get(
            party=user.party, action__desc__contains="APPROVE", model="INVOICE")
    return qs


# Function to REQUEST FINANCE for user type "SELLER"

def reqFin_transition(request):
    user = request.user
    if user.party.party_type == "SELLER":
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="REQUEST FINANCE", model="INVOICE")

    return obj


# Function to SUBMIT for user type "SELLER"

def submit_transition(request):
    user = request.user
    if user.party.party_type == "SELLER":
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="SUBMIT", model="INVOICE")
    return obj


# Function to REJECT for user type "BUYER"

def reject_transition(request):
    user = request.user
    if user.party.party_type == "BUYER":
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="REJECT", model="INVOICE")
    return obj


class InvoiceFlow(object):
    # workitems = workflowitems()
    stage = fsm.State(StateChoices, default=StateChoices.STATUS_DRAFT)

    def __init__(self, workflowitems):
        self.workflowitems = workflowitems

    @stage.setter()
    def _set_status_stage(self, value):
        self.workflowitems.flow_field = value

    @stage.getter()
    def _get_status(self):
        return self.workflowitems.flow_field

# <------------------------------------------|APF FLOW|--------------------------------------------->
# APPROVE

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AWAITING_SIGN_A)
    def approve_APF(self, request):

        user = request.user
        party = request.user.party
        obj = approve_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED_BY_BUYER
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.APPROVE, StateChoices.MAKER
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_APPROVED_BY_BUYER, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED_BY_BUYER
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.APPROVE, StateChoices.MAKER
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_APPROVED_BY_BUYER, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED_BY_BUYER
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.APPROVE, StateChoices.MAKER
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_APPROVED_BY_BUYER, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def approve_APF_SignA(self, request):

        user = request.user
        party = request.user.party
        obj = approve_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_APPROVED_BY_BUYER
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED_BY_BUYER
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.APPROVE, StateChoices.SIGN_A
            self.workflowitems.current_from_party = party
            self.workflowitems.current_to_party = self.workflowitems.user.party
            self.workflowitems.next_available_transitions = []

            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_APPROVED_BY_BUYER, type="INVOICE", event_user=user,
                                           interim_state=StateChoices.STATUS_APPROVED_BY_BUYER, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if party.party_type == "BUYER":
                cc.s_final = 'YES'
                cc.to_party = self.workflowitems.user.party
                cc.save()

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED_BY_BUYER
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.APPROVE, StateChoices.SIGN_A
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B]
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_APPROVED_BY_BUYER, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED_BY_BUYER
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.APPROVE, StateChoices.SIGN_A
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_APPROVED_BY_BUYER, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_B, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def approve_APF_SignB(self, request):

        user = request.user
        party = request.user.party
        obj = approve_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_APPROVED_BY_BUYER
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED_BY_BUYER
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.APPROVE, StateChoices.SIGN_B
            self.workflowitems.next_available_transitions = []
            self.workflowitems.current_from_party = party
            self.workflowitems.current_to_party = self.workflowitems.user.party
            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_APPROVED_BY_BUYER, type="INVOICE", event_user=user,
                                           interim_state=StateChoices.STATUS_APPROVED_BY_BUYER, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if party.party_type == "BUYER":
                cc.s_final = 'YES'
                cc.to_party = self.workflowitems.user.party
                cc.save()

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_C
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED_BY_BUYER
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.APPROVE, StateChoices.SIGN_B
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_C]
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_APPROVED_BY_BUYER, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_C, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_C, target=StateChoices.STATUS_APPROVED_BY_BUYER)
    def approve_APF_SignC(self, request):
        user = request.user
        party = request.user.party
        obj = approve_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_APPROVED_BY_BUYER
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED_BY_BUYER
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.APPROVE, StateChoices.SIGN_C
            self.workflowitems.next_available_transitions = []
            self.workflowitems.current_from_party = party
            self.workflowitems.current_to_party = self.workflowitems.user.party
            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_APPROVED_BY_BUYER, type="INVOICE", event_user=user,
                                           interim_state=StateChoices.STATUS_APPROVED_BY_BUYER, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if party.party_type == "BUYER":
                cc.s_final = 'YES'
                cc.to_party = self.workflowitems.user.party
                cc.save()

# REJECT

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AWAITING_SIGN_A)
    def reject_APF(self, request):
        user = request.user
        party = request.user.party
        obj = reject_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED_BY_BUYER
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.REJECT, StateChoices.MAKER
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_REJECTED_BY_BUYER, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED_BY_BUYER
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.REJECT, StateChoices.MAKER
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_REJECTED_BY_BUYER, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED_BY_BUYER
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.REJECT, StateChoices.MAKER
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_REJECTED_BY_BUYER, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def reject_APF_SignA(self, request):
        user = request.user
        party = request.user.party
        obj = reject_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_REJECTED_BY_BUYER
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED_BY_BUYER
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.REJECT, StateChoices.SIGN_A
            self.workflowitems.current_from_party = party
            self.workflowitems.current_to_party = self.workflowitems.user.party
            self.workflowitems.next_available_transitions = []

            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_REJECTED_BY_BUYER, type="INVOICE", event_user=user,
                                           interim_state=StateChoices.STATUS_REJECTED_BY_BUYER, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if party.party_type == "BUYER":
                cc.s_final = 'YES'
                cc.to_party = self.workflowitems.user.party
                cc.save()

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED_BY_BUYER
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.REJECT, StateChoices.SIGN_A
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_REJECTED_BY_BUYER, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED_BY_BUYER
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.REJECT, StateChoices.SIGN_A
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_REJECTED_BY_BUYER, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AWAITING_SIGN_C)
    def reject_APF_SignB(self, request):
        user = request.user
        party = request.user.party
        obj = reject_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_REJECTED_BY_BUYER
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED_BY_BUYER
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.REJECT, StateChoices.SIGN_B
            self.workflowitems.current_from_party = party
            self.workflowitems.current_to_party = self.workflowitems.user.party
            self.workflowitems.next_available_transitions = []

            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, to_state=StateChoices.STATUS_REJECTED_BY_BUYER, type="INVOICE", event_user=user,
                                           interim_state=StateChoices.STATUS_REJECTED_BY_BUYER, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, final="YES")

            if request.user.party.party_type == "BUYER":
                cc.s_final = 'YES'
                cc.to_party = self.workflowitems.user.party
                cc.save()

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_C
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED_BY_BUYER
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.REJECT, StateChoices.SIGN_B
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, to_state=StateChoices.STATUS_REJECTED_BY_BUYER, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_C, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_REJECTED_BY_BUYER)
    def reject_APF_SignC(self, request):
        user = request.user
        party = request.user.party
        obj = reject_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_REJECTED_BY_BUYER
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED_BY_BUYER
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.REJECT, StateChoices.SIGN_C
            self.workflowitems.current_from_party = party
            self.workflowitems.current_to_party = self.workflowitems.user.party
            self.workflowitems.next_available_transitions = []

            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_C, to_state=StateChoices.STATUS_REJECTED_BY_BUYER, type="INVOICE", event_user=user,
                                           interim_state=StateChoices.STATUS_REJECTED_BY_BUYER, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, final="YES")

            if request.user.party.party_type == "BUYER":
                cc.s_final = 'YES'
                cc.to_party = self.workflowitems.user.party
                cc.save()


# REQUEST FINANCE


    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AWAITING_SIGN_A)
    def REQ_FIN_APF(self, request):
        user = request.user
        party = request.user.party
        obj = reqFin_transition(request)
        type = workflowitems.objects.get(id=self.workflowitems.id)
        ws = gets_wf_item_id(self.workflowitems.id)
        program_type = type.invoice.pairing.program_id.program_type

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action = "REQUEST FINANCE"
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A]

            workevents.objects.create(workitems=ws, from_state=self.workflowitems.initial_state, to_state=StateChoices.STATUS_FINANCE_REQUESTED, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action = "REQUEST FINANCE"
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]

            workevents.objects.create(workitems=ws, from_state=self.workflowitems.initial_state, to_state=StateChoices.STATUS_FINANCE_REQUESTED, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action = "REQUEST FINANCE"
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=self.workflowitems.initial_state, to_state=StateChoices.STATUS_FINANCE_REQUESTED, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def REQ_FIN_APF_SignA(self, request):
        user = request.user
        party = request.user.party
        obj = reqFin_transition(request)
        type = workflowitems.objects.get(id=self.workflowitems.id)
        ws = gets_wf_item_id(self.workflowitems.id)
        bank = Parties.objects.get(party_type="BANK")
        program_type = type.invoice.pairing.program_id.program_type

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action = "REQUEST FINANCE"
            self.workflowitems.current_from_party = party
            self.workflowitems.current_to_party = bank
            self.workflowitems.next_available_transitions = []

            cc = workevents.objects.create(workitems=ws, from_state=self.workflowitems.initial_state, to_state=StateChoices.STATUS_FINANCE_REQUESTED, type="INVOICE", event_user=user,
                                           interim_state=StateChoices.STATUS_FINANCE_REQUESTED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "SELLER":
                cc.final = "YES"
                cc.to_party = bank
                cc.save()

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action = "REQUEST FINANCE"
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_FINANCE_REQUESTED, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action = "REQUEST FINANCE"
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_FINANCE_REQUESTED, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AWAITING_SIGN_C)
    def REQ_FIN_APF_SignB(self, request):
        user = request.user
        party = request.user.party
        obj = reqFin_transition(request)
        type = workflowitems.objects.get(id=self.workflowitems.id)
        ws = gets_wf_item_id(self.workflowitems.id)
        bank = Parties.objects.get(party_type="BANK")
        program_type = type.invoice.pairing.program_id.program_type

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action = "REQUEST FINANCE"
            self.workflowitems.current_from_party = party
            self.workflowitems.current_to_party = bank
            self.workflowitems.next_available_transitions = []

            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, to_state=StateChoices.STATUS_FINANCE_REQUESTED, type="INVOICE", event_user=user,
                                           interim_state=StateChoices.STATUS_FINANCE_REQUESTED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "SELLER":
                cc.final = "YES"
                cc.to_party = bank
                cc.save()

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_C
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action = "REQUEST FINANCE"
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, to_state=StateChoices.STATUS_FINANCE_REQUESTED, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_C, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_FINANCE_REQUESTED)
    def REQ_FIN_APF_SignC(self, request):
        user = request.user
        party = request.user.party
        obj = reqFin_transition(request)
        type = workflowitems.objects.get(id=self.workflowitems.id)
        ws = gets_wf_item_id(self.workflowitems.id)
        bank = Parties.objects.get(party_type="BANK")
        program_type = type.invoice.pairing.program_id.program_type

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action = "REQUEST FINANCE"
            self.workflowitems.current_from_party = party
            self.workflowitems.current_to_party = bank
            self.workflowitems.next_available_transitions = []

            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_C, to_state=StateChoices.STATUS_FINANCE_REQUESTED, type="INVOICE", event_user=user,
                                           interim_state=StateChoices.STATUS_FINANCE_REQUESTED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "SELLER":
                cc.final = "YES"
                cc.to_party = bank
                cc.save()
# SUBMIT

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AWAITING_SIGN_A)
    def Submit_APF(self, request):
        user = request.user
        party = request.user.party
        obj = submit_transition(request)
        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_AWAITING_BUYER_APPROVAL
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.SUBMIT, StateChoices.MAKER
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_REJECTED_BY_BUYER, to_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_AWAITING_BUYER_APPROVAL
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.SUBMIT, StateChoices.MAKER
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_REJECTED_BY_BUYER, to_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_AWAITING_BUYER_APPROVAL
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.SUBMIT, StateChoices.MAKER
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_REJECTED_BY_BUYER, to_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def Submit_APF_SignA(self, request):
        user = request.user
        party = request.user.party
        obj = submit_transition(request)

        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_BUYER_APPROVAL
            self.workflowitems.final_state = StateChoices.STATUS_AWAITING_BUYER_APPROVAL
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.SUBMIT, StateChoices.SIGN_A
            self.workflowitems.current_from_party = party
            self.workflowitems.current_to_party = self.workflowitems.invoice.pairing.program_id.party
            self.workflowitems.next_available_transitions = []

            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, type="INVOICE", event_user=user,
                                           interim_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "SELLER":
                cc.b_final = 'YES'
                cc.to_party = self.workflowitems.invoice.pairing.program_id.party
                cc.save()

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_AWAITING_BUYER_APPROVAL
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.SUBMIT, StateChoices.SIGN_A
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_AWAITING_BUYER_APPROVAL
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.SUBMIT, StateChoices.SIGN_A
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AWAITING_SIGN_C)
    def Submit_APF_SignB(self, request):
        user = request.user
        party = request.user.party
        obj = submit_transition(request)

        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_BUYER_APPROVAL
            self.workflowitems.final_state = StateChoices.STATUS_AWAITING_BUYER_APPROVAL
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.SUBMIT, StateChoices.SIGN_B
            self.workflowitems.current_from_party = party
            self.workflowitems.current_to_party = self.workflowitems.invoice.pairing.program_id.party
            self.workflowitems.next_available_transitions = []

            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, to_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, type="INVOICE", event_user=user,
                                           interim_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "SELLER":
                cc.b_final = 'YES'
                cc.to_party = self.workflowitems.invoice.pairing.program_id.party
                cc.save()

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_C
            self.workflowitems.final_state = StateChoices.STATUS_AWAITING_BUYER_APPROVAL
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.SUBMIT, StateChoices.SIGN_B
            self.workflowitems.current_from_party = self.workflowitems.current_to_party = party
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_C]

            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, to_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, type="INVOICE", event_user=user,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_C, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_AWAITING_BUYER_APPROVAL)
    def Submit_APF_SignC(self, request):
        user = request.user
        party = request.user.party
        obj = submit_transition(request)

        ws = gets_wf_item_id(self.workflowitems.id)

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_BUYER_APPROVAL
            self.workflowitems.final_state = StateChoices.STATUS_AWAITING_BUYER_APPROVAL
            self.workflowitems.action, self.workflowitems.subaction = StateChoices.SUBMIT, StateChoices.SIGN_C
            self.workflowitems.current_from_party = party
            self.workflowitems.current_to_party = self.workflowitems.invoice.pairing.program_id.party
            self.workflowitems.next_available_transitions = []

            cc = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_C, to_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, type="INVOICE", event_user=user,
                                           interim_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

            if request.user.party.party_type == "SELLER":
                cc.b_final = 'YES'
                cc.to_party = self.workflowitems.invoice.pairing.program_id.party
                cc.save()


# ARCHIVE


    @stage.transition(source=[StateChoices.STATUS_REJECTED_BY_BUYER, StateChoices.STATUS_FINANCE_REQUESTED, StateChoices.STATUS_APPROVED_BY_BUYER], target=StateChoices.STATUS_AWAITING_SIGN_A)
    def Archive_APF(self):
        user = self.workflowitems.event_users
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="ARCHIVE", model="INVOICE")

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_ARCHIVED
            self.workflowitems.action = "ARCHIVE"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_REJECTED_BY_BUYER, to_state=StateChoices.STATUS_ARCHIVED, type="INVOICE",
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_ARCHIVED
            self.workflowitems.action = "ARCHIVE"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_REJECTED_BY_BUYER, to_state=StateChoices.STATUS_ARCHIVED, type="INVOICE",
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_ARCHIVED
            self.workflowitems.action = "ARCHIVE"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_REJECTED_BY_BUYER, to_state=StateChoices.STATUS_ARCHIVED, type="INVOICE",
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_A, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def Archive_APF_SignA(self):
        user = self.workflowitems.event_users
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="ARCHIVE", model="INVOICE")

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_ARCHIVED
            self.workflowitems.final_state = StateChoices.STATUS_ARCHIVED
            self.workflowitems.action = "ARCHIVE"
            self.workflowitems.next_available_transitions = []
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_ARCHIVED, type="INVOICE",
                                      interim_state=StateChoices.STATUS_ARCHIVED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, final="YES")

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_ARCHIVED
            self.workflowitems.action = "ARCHIVE"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_ARCHIVED, type="INVOICE",
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_ARCHIVED
            self.workflowitems.action = "ARCHIVE"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_ARCHIVED, type="INVOICE",
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_B, target=StateChoices.STATUS_AWAITING_SIGN_C)
    def Archive_APF_SignB(self):
        user = self.workflowitems.event_users
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="ARCHIVE", model="INVOICE")

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True):
            self.workflowitems.interim_state = StateChoices.STATUS_ARCHIVED
            self.workflowitems.final_state = StateChoices.STATUS_ARCHIVED
            self.workflowitems.action = "ARCHIVE"
            self.workflowitems.next_available_transitions = []
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, to_state=StateChoices.STATUS_ARCHIVED, type="INVOICE",
                                      interim_state=StateChoices.STATUS_ARCHIVED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, final="YES")

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_C
            self.workflowitems.final_state = StateChoices.STATUS_ARCHIVED
            self.workflowitems.action = "ARCHIVE"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_C]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, to_state=StateChoices.STATUS_ARCHIVED, type="INVOICE",
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_C, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_C, target=StateChoices.STATUS_ARCHIVED)
    def Archive_APF_SignC(self):
        user = self.workflowitems.event_users
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="ARCHIVE", model="INVOICE")

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True):
            self.workflowitems.interim_state = StateChoices.STATUS_ARCHIVED
            self.workflowitems.final_state = StateChoices.STATUS_ARCHIVED
            self.workflowitems.action = "ARCHIVE"
            self.workflowitems.next_available_transitions = []
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_C, to_state=StateChoices.STATUS_ARCHIVED, type="INVOICE",
                                      interim_state=StateChoices.STATUS_ARCHIVED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, final="YES")


# <------------------------------------|RF and DF FLOW|--FOR INVOICE SUBMIT ------------------------------------------->

    @stage.transition(source=StateChoices.STATUS_DRAFT, target=StateChoices.STATUS_AWAITING_SIGN_A)
    def submit__draft(self, request):
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
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = []
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_C, to_state=StateChoices.STATUS_FINANCE_REQUESTED, type="INVOICE", user=user,
                                      interim_state=StateChoices.STATUS_FINANCE_REQUESTED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, final="YES")

# RETURN TRANSITION

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_C, target=StateChoices.STATUS_DRAFT)
    def Return_Invoice(self, request):
        user = request.user
        self.workflowitems.interim_state = StateChoices.STATUS_INITIAL_STATE
        self.workflowitems.final_state = StateChoices.STATUS_INITIAL_STATE
        self.workflowitems.action = "RETURN"
        ws = workflowitems.objects.get(id=self.workflowitems.id)
        workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_C, to_state=StateChoices.STATUS_INITIAL_STATE, type="INVOICE", event_user=user,
                                  interim_state=StateChoices.STATUS_INITIAL_STATE, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)
