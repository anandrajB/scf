# # django fsm flows using djano-viewflow package == 2.0a02
from transaction.states import StateChoices
from transaction.models import workevents, workflowitems
from viewflow import fsm
from accounts.models import signatures
from accounts.models import userprocessauth


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

# <------------------------------------------|APF FLOW|--------------------------------------------->
# APPROVE

    @stage.transition(source=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, target=StateChoices.STATUS_AWAITING_SIGN_A)
    def approve_APF(self):

        user = self.workflowitems.event_users
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="APPROVE", model="INVOICE")
        type = workflowitems.objects.get(id=self.workflowitems.id)
        program_type = type.invoice.pairing.program_type.program_type

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED_BY_BUYER
            self.workflowitems.action = "APPROVE"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_APPROVED_BY_BUYER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED_BY_BUYER
            self.workflowitems.action = "APPROVE"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_APPROVED_BY_BUYER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED_BY_BUYER
            self.workflowitems.action = "APPROVE"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_APPROVED_BY_BUYER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_A, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def approve_APF_SignA(self):

        user = self.workflowitems.event_users
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="APPROVE", model="INVOICE")
        type = workflowitems.objects.get(id=self.workflowitems.id)
        program_type = type.invoice.pairing.program_type.program_type

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_APPROVED_BY_BUYER
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED_BY_BUYER
            self.workflowitems.action = "APPROVE"
            self.workflowitems.next_available_transitions = []
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_APPROVED_BY_BUYER,
                                      interim_state=StateChoices.STATUS_APPROVED_BY_BUYER, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, final="YES")

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED_BY_BUYER
            self.workflowitems.action = "APPROVE"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_APPROVED_BY_BUYER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED_BY_BUYER
            self.workflowitems.action = "APPROVE"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_APPROVED_BY_BUYER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_B, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def approve_APF_SignB(self):

        user = self.workflowitems.event_users
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="APPROVE", model="INVOICE")
        type = workflowitems.objects.get(id=self.workflowitems.id)
        program_type = type.invoice.pairing.program_type.program_type

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_APPROVED_BY_BUYER
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED_BY_BUYER
            self.workflowitems.action = "APPROVE"
            self.workflowitems.next_available_transitions = []
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_APPROVED_BY_BUYER,
                                      interim_state=StateChoices.STATUS_APPROVED_BY_BUYER, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, final="YES")

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_C
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED_BY_BUYER
            self.workflowitems.action = "APPROVE"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_C]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_APPROVED_BY_BUYER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_C, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transtion(source=StateChoices.STATUS_AWAITING_SIGN_C, target=StateChoices.STATUS_APPROVED_BY_BUYER)
    def approve_APF_SignC(self):
        user = self.workflowitems.event_users
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="APPROVE", model="INVOICE")
        type = workflowitems.objects.get(id=self.workflowitems.id)
        program_type = type.invoice.pairing.program_type.program_type

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_APPROVED_BY_BUYER
            self.workflowitems.final_state = StateChoices.STATUS_APPROVED_BY_BUYER
            self.workflowitems.action = "APPROVE"
            self.workflowitems.next_available_transitions = []
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_APPROVED_BY_BUYER,
                                      interim_state=StateChoices.STATUS_APPROVED_BY_BUYER, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, final="YES")

# REJECT

    @stage.transition(source=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, target=StateChoices.STATUS_AWAITING_SIGN_A)
    def reject_APF(self):
        user = self.workflowitems.event_users
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="REJECT", model="INVOICE")
        type = workflowitems.objects.get(id=self.workflowitems.id)
        program_type = type.invoice.pairing.program_type.program_type

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED_BY_BUYER
            self.workflowitems.action = "REJECT"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_REJECTED_BY_BUYER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED_BY_BUYER
            self.workflowitems.action = "REJECT"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_REJECTED_BY_BUYER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED_BY_BUYER
            self.workflowitems.action = "REJECT"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, to_state=StateChoices.STATUS_REJECTED_BY_BUYER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_A, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def reject_APF_SignA(self):
        user = self.workflowitems.event_users
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="REJECT", model="INVOICE")
        type = workflowitems.objects.get(id=self.workflowitems.id)
        program_type = type.invoice.pairing.program_type.program_type

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_REJECTED_BY_BUYER
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED_BY_BUYER
            self.workflowitems.action = "REJECT"
            self.workflowitems.next_available_transitions = []
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_REJECTED_BY_BUYER,
                                      interim_state=StateChoices.STATUS_REJECTED_BY_BUYER, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, final="YES")

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED_BY_BUYER
            self.workflowitems.action = "REJECT"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_REJECTED_BY_BUYER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED_BY_BUYER
            self.workflowitems.action = "REJECT"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_REJECTED_BY_BUYER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_B, target=StateChoices.STATUS_AWAITING_SIGN_C)
    def reject_APF_SignB(self):
        user = self.workflowitems.event_users
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="REJECT", model="INVOICE")
        type = workflowitems.objects.get(id=self.workflowitems.id)
        program_type = type.invoice.pairing.program_type.program_type

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_REJECTED_BY_BUYER
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED_BY_BUYER
            self.workflowitems.action = "REJECT"
            self.workflowitems.next_available_transitions = []
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, to_state=StateChoices.STATUS_REJECTED_BY_BUYER,
                                      interim_state=StateChoices.STATUS_REJECTED_BY_BUYER, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, final="YES")

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_C
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED_BY_BUYER
            self.workflowitems.action = "REJECT"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_C]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, to_state=StateChoices.STATUS_REJECTED_BY_BUYER,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_C, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_C, target=StateChoices.STATUS_REJECTED_BY_BUYER)
    def reject_APF_SignC(self):
        user = self.workflowitems.event_users
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="REJECT", model="INVOICE")
        type = workflowitems.objects.get(id=self.workflowitems.id)
        program_type = type.invoice.pairing.program_type.program_type

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_REJECTED_BY_BUYER
            self.workflowitems.final_state = StateChoices.STATUS_REJECTED_BY_BUYER
            self.workflowitems.action = "REJECT"
            self.workflowitems.next_available_transitions = []
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_C, to_state=StateChoices.STATUS_REJECTED_BY_BUYER,
                                      interim_state=StateChoices.STATUS_REJECTED_BY_BUYER, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, final="YES")

# REQUEST FINANCE

    @stage.transition(source=[StateChoices.STATUS_APPROVED_BY_BUYER, StateChoices.STATUS_FINANCE_REJECTED], target=StateChoices.STATUS_AWAITING_SIGN_A)
    def REQ_FIN_APF(self):
        user = self.workflowitems.event_users
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="REQUEST FINANCE", model="INVOICE")
        type = workflowitems.objects.get(id=self.workflowitems.id)
        program_type = type.invoice.pairing.program_type.program_type

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action = "REQUEST FINANCE"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_APPROVED_BY_BUYER, to_state=StateChoices.STATUS_FINANCE_REQUESTED,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action = "REQUEST FINANCE"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_APPROVED_BY_BUYER, to_state=StateChoices.STATUS_FINANCE_REQUESTED,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action = "REQUEST FINANCE"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_APPROVED_BY_BUYER, to_state=StateChoices.STATUS_FINANCE_REQUESTED,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_A, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def REQ_FIN_APF_SignA(self):
        user = self.workflowitems.event_users
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="REQUEST FINANCE", model="INVOICE")
        type = workflowitems.objects.get(id=self.workflowitems.id)
        program_type = type.invoice.pairing.program_type.program_type

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action = "REQUEST FINANCE"
            self.workflowitems.next_available_transitions = []
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_FINANCE_REQUESTED,
                                      interim_state=StateChoices.STATUS_FINANCE_REQUESTED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, final="YES")

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action = "REQUEST FINANCE"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_FINANCE_REQUESTED,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action = "REQUEST FINANCE"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_FINANCE_REQUESTED,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_B, target=StateChoices.STATUS_AWAITING_SIGN_C)
    def REQ_FIN_APF_SignB(self):
        user = self.workflowitems.event_users
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="REQUEST FINANCE", model="INVOICE")
        type = workflowitems.objects.get(id=self.workflowitems.id)
        program_type = type.invoice.pairing.program_type.program_type

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action = "REQUEST FINANCE"
            self.workflowitems.next_available_transitions = []
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, to_state=StateChoices.STATUS_FINANCE_REQUESTED,
                                      interim_state=StateChoices.STATUS_FINANCE_REQUESTED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, final="YES")

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_C
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action = "REQUEST FINANCE"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_C]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, to_state=StateChoices.STATUS_FINANCE_REQUESTED,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_C, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_C, target=StateChoices.STATUS_FINANCE_REQUESTED)
    def REQ_FIN_APF_SignC(self):
        user = self.workflowitems.event_users
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="REQUEST FINANCE", model="INVOICE")
        type = workflowitems.objects.get(id=self.workflowitems.id)
        program_type = type.invoice.pairing.program_type.program_type

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action = "REQUEST FINANCE"
            self.workflowitems.next_available_transitions = []
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_C, to_state=StateChoices.STATUS_FINANCE_REQUESTED,
                                      interim_state=StateChoices.STATUS_FINANCE_REQUESTED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

# SUBMIT

    @stage.transition(source=StateChoices.STATUS_REJECTED_BY_BUYER, target=StateChoices.STATUS_AWAITING_SIGN_A)
    def Submit_APF(self):
        user = self.workflowitems.event_users
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="SUBMIT", model="INVOICE")
        type = workflowitems.objects.get(id=self.workflowitems.id)
        program_type = type.invoice.pairing.program_type.program_type

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_AWAITING_BUYER_APPROVAL
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_REJECTED_BY_BUYER, to_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_AWAITING_BUYER_APPROVAL
            self.workflowitems.action = "SUMBIT"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_REJECTED_BY_BUYER, to_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_AWAITING_BUYER_APPROVAL
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_REJECTED_BY_BUYER, to_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_A, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def Submit_APF_SignA(self):
        user = self.workflowitems.event_users
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="SUBMIT", model="INVOICE")
        type = workflowitems.objects.get(id=self.workflowitems.id)
        program_type = type.invoice.pairing.program_type.program_type

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_BUYER_APPROVAL
            self.workflowitems.final_state = StateChoices.STATUS_AWAITING_BUYER_APPROVAL
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = []
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL,
                                      interim_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, final="YES")

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_AWAITING_BUYER_APPROVAL
            self.workflowitems.action = "SUMBIT"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_AWAITING_BUYER_APPROVAL
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_B, target=StateChoices.STATUS_AWAITING_SIGN_C)
    def Submit_APF_SignB(self):
        user = self.workflowitems.event_users
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="SUBMIT", model="INVOICE")
        type = workflowitems.objects.get(id=self.workflowitems.id)
        program_type = type.invoice.pairing.program_type.program_type

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_BUYER_APPROVAL
            self.workflowitems.final_state = StateChoices.STATUS_AWAITING_BUYER_APPROVAL
            self.workflowitems.action = "SUMBIT"
            self.workflowitems.next_available_transitions = []
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, to_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL,
                                      interim_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, final="YES")

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_C
            self.workflowitems.final_state = StateChoices.STATUS_AWAITING_BUYER_APPROVAL
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_C]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, to_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_C, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_B, target=StateChoices.STATUS_AWAITING_BUYER_APPROVAL)
    def Submit_APF_SignC(self):
        user = self.workflowitems.event_users
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="SUBMIT", model="INVOICE")
        type = workflowitems.objects.get(id=self.workflowitems.id)
        program_type = type.invoice.pairing.program_type.program_type

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_BUYER_APPROVAL
            self.workflowitems.final_state = StateChoices.STATUS_AWAITING_BUYER_APPROVAL
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = []
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_C, to_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL,
                                      interim_state=StateChoices.STATUS_AWAITING_BUYER_APPROVAL, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, final="YES")

# ARCHIVE

    @stage.transition(source=[StateChoices.STATUS_REJECTED_BY_BUYER, StateChoices.STATUS_FINANCE_REQUESTED, StateChoices.STATUS_APPROVED_BY_BUYER], target=StateChoices.STATUS_AWAITING_SIGN_A)
    def Archive_APF(self):
        user = self.workflowitems.event_users
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="ARCHIVE", model="INVOICE")
        type = workflowitems.objects.get(id=self.workflowitems.id)
        program_type = type.invoice.pairing.program_type.program_type

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_ARCHIVED
            self.workflowitems.action = "ARCHIVE"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_REJECTED_BY_BUYER, to_state=StateChoices.STATUS_ARCHIVED,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_ARCHIVED
            self.workflowitems.action = "ARCHIVE"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_REJECTED_BY_BUYER, to_state=StateChoices.STATUS_ARCHIVED,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_ARCHIVED
            self.workflowitems.action = "ARCHIVE"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_REJECTED_BY_BUYER, to_state=StateChoices.STATUS_ARCHIVED,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_A, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def Archive_APF_SignA(self):
        user = self.workflowitems.event_users
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="ARCHIVE", model="INVOICE")
        type = workflowitems.objects.get(id=self.workflowitems.id)
        program_type = type.invoice.pairing.program_type.program_type

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_ARCHIVED
            self.workflowitems.final_state = StateChoices.STATUS_ARCHIVED
            self.workflowitems.action = "ARCHIVE"
            self.workflowitems.next_available_transitions = []
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_ARCHIVED,
                                      interim_state=StateChoices.STATUS_ARCHIVED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, final="YES")

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_ARCHIVED
            self.workflowitems.action = "ARCHIVE"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_ARCHIVED,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_ARCHIVED
            self.workflowitems.action = "ARCHIVE"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_ARCHIVED,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_B, target=StateChoices.STATUS_AWAITING_SIGN_C)
    def Archive_APF_SignB(self):
        user = self.workflowitems.event_users
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="ARCHIVE", model="INVOICE")
        type = workflowitems.objects.get(id=self.workflowitems.id)
        program_type = type.invoice.pairing.program_type.program_type

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_ARCHIVED
            self.workflowitems.final_state = StateChoices.STATUS_ARCHIVED
            self.workflowitems.action = "ARCHIVE"
            self.workflowitems.next_available_transitions = []
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, to_state=StateChoices.STATUS_ARCHIVED,
                                      interim_state=StateChoices.STATUS_ARCHIVED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, final="YES")

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_C
            self.workflowitems.final_state = StateChoices.STATUS_ARCHIVED
            self.workflowitems.action = "ARCHIVE"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_C]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, to_state=StateChoices.STATUS_ARCHIVED,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_C, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_C, target=StateChoices.STATUS_ARCHIVED)
    def Archive_APF_SignC(self):
        user = self.workflowitems.event_users
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="ARCHIVE", model="INVOICE")
        type = workflowitems.objects.get(id=self.workflowitems.id)
        program_type = type.invoice.pairing.program_type.program_type

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True and program_type == "APF"):
            self.workflowitems.interim_state = StateChoices.STATUS_ARCHIVED
            self.workflowitems.final_state = StateChoices.STATUS_ARCHIVED
            self.workflowitems.action = "ARCHIVE"
            self.workflowitems.next_available_transitions = []
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_C, to_state=StateChoices.STATUS_ARCHIVED,
                                      interim_state=StateChoices.STATUS_ARCHIVED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, final="YES")

#


# <------------------------------------|RF and DF FLOW|--------------------------------------------->

    @stage.transition(source=StateChoices.STATUS_DRAFT, target=StateChoices.STATUS_AWAITING_SIGN_A)
    def submit__draft(self):
        user = self.workflowitems.event_users
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="SUBMIT", model="INVOICE")
        type = workflowitems.objects.get(id=self.workflowitems.id)
        program_type = type.invoice.pairing.program_type.program_type

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True and (program_type == "RF" or program_type == "DF")):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_FINANCE_REQUESTED,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True and (program_type == "RF" or program_type == "DF")):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_FINANCE_REQUESTED,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True and (program_type == "RF" or program_type == "DF")):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_A
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_A, StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_FINANCE_REQUESTED,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_A, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_A, target=StateChoices.STATUS_AWAITING_SIGN_B)
    def submit__SignA(self):
        user = self.workflowitems.event_users
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="SUBMIT", model="INVOICE")
        type = workflowitems.objects.get(id=self.workflowitems.id)
        program_type = type.invoice.pairing.program_type.program_type

        if(obj.sign_a == True and obj.sign_b != True and obj.sign_c != True and (program_type == "RF" or program_type == "DF")):

            self.workflowitems.interim_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = []
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_FINANCE_REQUESTED,
                                      interim_state=StateChoices.STATUS_FINANCE_REQUESTED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, final="YES")

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True and (program_type == "RF" or program_type == "DF")):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_FINANCE_REQUESTED,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True and (program_type == "RF" or program_type == "DF")):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_B
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_B, StateChoices.STATUS_AWAITING_SIGN_C]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_A, to_state=StateChoices.STATUS_FINANCE_REQUESTED,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_B, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_B, target=StateChoices.STATUS_AWAITING_SIGN_C)
    def submit__SignB(self):
        user = self.workflowitems.event_users
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="SUBMIT", model="INVOICE")
        type = workflowitems.objects.get(id=self.workflowitems.id)
        program_type = type.invoice.pairing.program_type.program_type

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c != True and (program_type == "RF" or program_type == "DF")):

            self.workflowitems.interim_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = []
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, to_state=StateChoices.STATUS_FINANCE_REQUESTED,
                                      interim_state=StateChoices.STATUS_FINANCE_REQUESTED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party, final="YES")

        elif(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True and (program_type == "RF" or program_type == "DF")):

            self.workflowitems.interim_state = StateChoices.STATUS_AWAITING_SIGN_C
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = [
                StateChoices.STATUS_AWAITING_SIGN_C]
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_B, to_state=StateChoices.STATUS_FINANCE_REQUESTED,
                                      interim_state=StateChoices.STATUS_AWAITING_SIGN_C, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)

    @stage.transition(source=StateChoices.STATUS_AWAITING_SIGN_C, target=StateChoices.STATUS_FINANCE_REQUESTED)
    def submit__SignC(self):
        user = self.workflowitems.event_users
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="SUBMIT", model="INVOICE")
        type = workflowitems.objects.get(id=self.workflowitems.id)
        program_type = type.invoice.pairing.program_type.program_type

        if(obj.sign_a == True and obj.sign_b == True and obj.sign_c == True and (program_type == "RF" or program_type == "DF")):

            self.workflowitems.interim_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.final_state = StateChoices.STATUS_FINANCE_REQUESTED
            self.workflowitems.action = "SUBMIT"
            self.workflowitems.next_available_transitions = []
            ws = workflowitems.objects.get(id=self.workflowitems.id)
            workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_AWAITING_SIGN_C, to_state=StateChoices.STATUS_FINANCE_REQUESTED,
                                      interim_state=StateChoices.STATUS_FINANCE_REQUESTED, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)
