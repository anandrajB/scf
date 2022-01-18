from random import choices
from django.db import models
from datetime import date
from django.dispatch import receiver
from django_fsm import FSMField, transition
from transaction.permission import is_approver, is_uploader
from django.contrib.auth import get_user_model

#  MODELS RELATED TO TRANSACTION


class submodels(models.Model):
    description = models.CharField(max_length=35)
    api_route = models.CharField(max_length=55)


class Transitionpartytype(models.Model):
    description = models.CharField(max_length=55)


# PROGRAM MODEL

class Programs(models.Model):

    finance_request_type = [
        ('AUTOMATIC', 'AUTOMATIC'),
        ('ON_REQUEST', 'ON_REQUEST')
    ]

    interest_choices = [
        ('FIXED', 'FIXED'),
        ('FLOATING', 'FLOATING')
    ]

    interest_rate_type_choices = [
        ('LIBOR', 'LIBOR'),
        ('EURIBOR', 'EURIBOR'),
        ('SOFOR', 'SOFOR')
    ]

    program_type = [
        ('ALL', 'ALL'),
        ('APF', 'APF'),
        ('RF', 'RF'),
        ('DF', 'DF')
    ]

    party = models.ForeignKey("accounts.Parties", on_delete=models.CASCADE)
    program_type = models.CharField(
        choices=program_type, default='*', max_length=10)
    finance_request_type = models.CharField(
        choices=finance_request_type, max_length=15, default=None)
    limit_currency = models.CharField(max_length=3)
    total_limit_amount = models.DecimalField(max_digits=7, decimal_places=2)
    finance_currency = models.CharField(max_length=3)
    settlement_currency = models.CharField(max_length=3)
    expiry_date = models.DateField(default=date.today)
    max_finance_percentage = models.DecimalField(
        max_digits=5, decimal_places=2)
    max_invoice_age_for_funding = models.IntegerField()
    max_age_for_repayment = models.IntegerField()
    minimum_period = models.IntegerField()
    maximum_period = models.IntegerField()
    maximum_amount = models.DecimalField(max_digits=5, decimal_places=2)
    minimum_amount = models.DecimalField(max_digits=5, decimal_places=2)
    financed_amount = models.DecimalField(max_digits=5, decimal_places=2)
    balance_amount = models.DecimalField(max_digits=5, decimal_places=2)
    grace_period = models.IntegerField()
    interest_type = models.CharField(
        choices=interest_choices, default=None, max_length=15)
    interest_rate_type = models.CharField(
        choices=interest_rate_type_choices, max_length=15, default=None)
    interest_rate = models.DecimalField(max_digits=6, decimal_places=2)
    margin = models.DecimalField(max_digits=5, decimal_places=2)


# FUNDING REQUEST MODEL

class FundingRequest(models.Model):
    program = models.ForeignKey(Programs, on_delete=models.CASCADE)
    total_amount = models.IntegerField()
    financed_amount = models.DecimalField(max_digits=8, decimal_places=2)
    balance_amount = models.DecimalField(max_digits=8, decimal_places=2)
    due_date = models.DateField(default=date.today)

    def __str__(self):
        return "%s - %s -%s  due date of %s" % (self.program, self.total_amount, self.financed_amount, self.financed_amount)


# PAIRINGS

class Pairings(models.Model):

    finance_request_type = [
        ('AUTOMATIC', 'AUTOMATIC'),
        ('ON_REQUEST', 'ON_REQUEST')
    ]

    interest_choices = [
        ('FIXED', 'FIXED'),
        ('FLOATING', 'FLOATING')
    ]

    interest_rate_type_choices = [
        ('LIBOR', 'LIBOR'),
        ('EURIBOR', 'EURIBOR'),
        ('SOFOR', 'SOFOR')
    ]

    program_type = models.ForeignKey(Programs, on_delete=models.DO_NOTHING)
    counterparty_id = models.ForeignKey(
        "accounts.Parties", on_delete=models.CASCADE)
    finance_request = models.CharField(
        choices=finance_request_type, max_length=15, default=None)
    currency = models.ForeignKey(
        "accounts.Currencies", on_delete=models.DO_NOTHING, related_name='pairingscurrency')
    total_limit = models.DecimalField(max_digits=8, decimal_places=2)
    finance_currency_type = models.ForeignKey(
        "accounts.Currencies", on_delete=models.DO_NOTHING, related_name='financedcurrency')
    settlement_currency_type = models.ForeignKey(
        "accounts.Currencies", on_delete=models.CASCADE)
    expiry_date = models.DateField(default=date.today)
    max_finance_percentage = models.DecimalField(
        max_digits=8, decimal_places=2)
    max_invoice_age_for_funding = models.IntegerField()
    max_age_for_repayment = models.IntegerField()
    minimum_period = models.IntegerField()
    maximum_period = models.IntegerField()
    minimum_amount_currency = models.CharField(max_length=3)
    minimum_amount = models.DecimalField(max_digits=8, decimal_places=2)
    maximum_amount = models.DecimalField(max_digits=8, decimal_places=2)
    financed_amount = models.DecimalField(max_digits=8, decimal_places=2)
    balance_amount = models.DecimalField(max_digits=8, decimal_places=2)
    grace_period = models.IntegerField()
    interest_type = models.CharField(
        choices=interest_choices, default=None, max_length=15)
    interest_rate_type = models.CharField(
        choices=interest_rate_type_choices, max_length=15, default=None)
    interest_rate = models.DecimalField(max_digits=8, decimal_places=2)
    margin = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return "%s - %s" % (self.finance_request, self.financed_amount)


# ACTIONS

class Actions(models.Model):
    description = models.CharField(max_length=255)
    bank = models.BooleanField(default=False)
    customer = models.BooleanField(default=False)


# WORKFLOW ITEMS MODEL

class workflowitems(models.Model):

    STATUS_DRAFT = 'DRAFT'
    STATUS_AW_APPROVAL = 'AWAITING_APPROVAL'
    STATUS_AW_ACCEPT = 'AWAITING_ACCEPTANCE'
    STATUS_ACCEPTED = 'ACCEPTED'
    STATUS_APPROVED = 'APPROVED'
    STATUS_REJECTED = 'REJECTED'
    STATUS_FINANCE_REQUESTED = 'FINANCE_REQUESTED'
    STATUS_FINANCED = 'FINANCED'
    STATUS_FINANCE_REJECTED = 'FINANCE_REJECTED'
    STATUS_SETTLED = 'SETTLED'
    STATUS_OVERDUE = 'OVERDUE'
    STATUS_AWAITING_SIGN_A = 'AWAITING_SIGN_A'
    STATUS_AWAITING_SIGN_B = 'AWAITING_SIGN_B'
    STATUS_AWAITING_SIGN_C = 'AWAITING_SIGN_C'
    STATUS_DELETED = 'DELETED'

    STATE_TYPE = [
        (STATUS_DRAFT, 'DRAFT'),
        (STATUS_AW_APPROVAL, 'AWAITING_APPROVAL'),
        (STATUS_AW_ACCEPT, 'AWAITING_ACCEPTANCE'),
        (STATUS_ACCEPTED, 'ACCEPTED'),
        (STATUS_APPROVED, 'APPROVED'),
        (STATUS_REJECTED, 'REJECTED'),
        (STATUS_FINANCE_REQUESTED, 'FINANCE_REQUESTED'),
        (STATUS_FINANCED, 'FINANCED'),
        (STATUS_FINANCE_REJECTED, 'FINANCE_REJECTED'),
        (STATUS_SETTLED, 'SETTLED'),
        (STATUS_OVERDUE, 'OVERDUE'),
        (STATUS_AWAITING_SIGN_A, 'AWAITING_SIGN_A'),
        (STATUS_AWAITING_SIGN_B, 'AWAITING_SIGN_B'),
        (STATUS_AWAITING_SIGN_C, 'AWAITING_SIGN_C'),
        (STATUS_DELETED, 'DELETED')
    ]

    created_date = models.DateTimeField(auto_now_add=True)
    program = models.OneToOneField(Programs, on_delete=models.CASCADE)
    initial_state = FSMField(choices=STATE_TYPE, default=STATUS_DRAFT)
    reject_state = FSMField(choices=STATE_TYPE, default=STATUS_AW_ACCEPT)
    accept_state = FSMField(choices=STATE_TYPE, default=STATUS_AW_ACCEPT)
    return_state = FSMField(choices=STATE_TYPE)
    interim_state = models.CharField(max_length=25, default=STATUS_DRAFT)
    final_state = models.CharField(
        choices=STATE_TYPE, default=STATUS_DRAFT, max_length=50)
    next_available_transitions = models.CharField(max_length=255)
    event_users = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name='customername')
    current_from_party = models.ForeignKey(
        "accounts.Parties", on_delete=models.DO_NOTHING, related_name='from_party')
    current_to_party = models.ForeignKey(
        "accounts.Parties", on_delete=models.DO_NOTHING, related_name='to_party')
    action = models.CharField(max_length=25, default='SUBMIT')

# --------------------------------------------------------------------------------------------------------

    # TRANSITION FOR WORKFLOW'S

# --------------------------------------------------------------------------------------------------------

    # ACTION DELETE

    @transition(field=initial_state, source=['*'], target=STATUS_DELETED, custom=({'button_name': 'Cancel'}),)
    def delete(self):
        self.final_state = 'DELETED'
        self.interim_state = 'DELETED'
        self.action = 'DELETE'
        ws = workflowitems.objects.get(id=self.id)
        workevents.objects.create(workitems=ws, from_state=self.final_state,
                                  to_state=self.final_state, interim_state=self.interim_state, from_party=self.current_from_party, to_party=self.current_to_party)

    # /-- ACTION : SUBMIT  --/

    @transition(field=initial_state, source=[STATUS_DRAFT, STATUS_AW_ACCEPT], target=STATUS_AWAITING_SIGN_A, custom=({'button_name': 'Cancel'}),)
    def submit(self):
        self.final_state = 'AWAITING_APPROVAL'
        self.interim_state = 'AWAITING_SIGN_A'
        self.action = 'SUBMIT'
        ws = workflowitems.objects.get(id=self.id)
        workevents.objects.create(workitems=ws, from_state='DRAFT', to_state='AWAITING_APPROVAL',
                                  interim_state='AWAITING_SIGN_A', from_party=self.current_from_party, to_party=self.current_to_party)

    @transition(field=initial_state, source=STATUS_AWAITING_SIGN_A, target=STATUS_AWAITING_SIGN_B)
    def submit_sign_a(self):
        self.final_state = 'AWAITING_APPROVAL'
        self.interim_state = 'AWAITING_SIGN_B'
        self.action = 'SUBMIT_SIGN_A'
        ws = workflowitems.objects.get(id=self.id)
        workevents.objects.create(workitems=ws, from_state='AWAITING_SIGN_A',
                                  to_state='AWAITING_APPROVAL', interim_state='AWAITING_SIGN_B', from_party=self.current_from_party, to_party=self.current_to_party)

    @transition(field=initial_state, source=STATUS_AWAITING_SIGN_B, target=STATUS_AWAITING_SIGN_C, permission=is_approver)
    def submit_sign_b(self):
        self.final_state = 'AWAITING_APPROVAL'
        self.interim_state = 'AWAITING_SIGN_C'
        self.action = 'SUBMIT_SIGN_B'
        ws = workflowitems.objects.get(id=self.id)
        workevents.objects.create(workitems=ws, from_state='AWAITING_SIGN_B',
                                  to_state='AWAITING_APPROVAL', interim_state='AWAITING_SIGN_C', from_party=self.current_from_party, to_party=self.current_to_party)

    @transition(field=initial_state, source=STATUS_AWAITING_SIGN_C, target=STATUS_AW_APPROVAL,)
    def submit_sign_c(self):
        self.final_state = "AWAITING_APPROVAL"
        self.interim_state = "AWAITING_APPROVAL"
        self.action = 'SUBMIT_SIGN_C'
        ws = workflowitems.objects.get(id=self.id)
        workevents.objects.create(workitems=ws, from_state='AWAITING_SIGN_C',
                                  to_state='AWAITING_APPROVAL', interim_state='AWAITING_APPROVAL', from_party=self.current_from_party, to_party=self.current_to_party)

    # /-- ACTION : REJECT  --/

    @transition(field=reject_state, source=STATUS_AW_ACCEPT, target=STATUS_AWAITING_SIGN_A, permission=is_approver)
    def reject(self):
        self.final_state = "REJECTED"
        self.interim_state = "AWAITING_SIGN_A"
        self.action = 'REJECT'
        ws = workflowitems.objects.get(id=self.id)
        workevents.objects.create(workitems=ws, from_state='AWAITING ACCEPTANCE',
                                  to_state='REJECTED', interim_state='AWAITING_SIGN_A')

    @transition(field=reject_state, source=STATUS_AWAITING_SIGN_A, target=STATUS_AWAITING_SIGN_B, permission=is_approver)
    def reject_sign_a(self):
        self.final_state = "REJECTED"
        self.interim_state = "AWAITING_SIGN_B"
        self.action = 'REJECT_SIGN_A'
        ws = workflowitems.objects.get(id=self.id)
        workevents.objects.create(workitems=ws, from_state='AWAITING_SIGN_A',
                                  to_state='REJECTED', interim_state='AWAITING_SIGN_B')

    @transition(field=reject_state, source=STATUS_AWAITING_SIGN_B, target=STATUS_AWAITING_SIGN_C, permission=is_approver)
    def reject_sign_b(self):
        self.final_state = "REJECTED"
        self.interim_state = "AWAITING_SIGN_C"
        self.action = 'REJECT_SIGN_B'
        ws = workflowitems.objects.get(id=self.id)
        workevents.objects.create(workitems=ws, from_state='AWAITING_SIGN_B',
                                  to_state='REJECTED', interim_state='AWAITING_SIGN_C')

    @transition(field=reject_state, source=STATUS_AWAITING_SIGN_C, target=STATUS_REJECTED, permission=is_approver)
    def reject_sign_c(self):
        self.final_state = "REJECTED"
        self.interim_state = "REJECTED"
        self.action = 'REJECT_SIGN_C'
        ws = workflowitems.objects.get(id=self.id)
        workevents.objects.create(workitems=ws, from_state='AWAITING_SIGN_C',
                                  to_state='REJECTED', interim_state='REJECTED')

    # /-- ACTION : ACCEPT  --/

    @transition(field=accept_state, source=STATUS_AW_ACCEPT, target=STATUS_AWAITING_SIGN_A, permission=is_approver)
    def accept(self):
        self.final_state = "ACCEPTED"
        self.interim_state = "AWAITING_SIGN_A"
        self.action = "ACCEPT"
        ws = workflowitems.objects.get(id=self.id)
        workevents.objects.create(workitems=ws, from_state='AWAITING_ACCEPTANCE',
                                  to_state='ACCEPTED', interim_state='AWAITING_SIGN_A')

    @transition(field=accept_state, source=STATUS_AWAITING_SIGN_A, target=STATUS_AWAITING_SIGN_B, permission=is_approver)
    def accept_sign_a(self):
        self.final_state = "ACCEPTED"
        self.interim_state = "AWAITING_SIGN_B"
        self.action = "ACCEPT_SIGN_A"
        ws = workflowitems.objects.get(id=self.id)
        workevents.objects.create(workitems=ws, from_state='AWAITING_SIGN_A',
                                  to_state='ACCEPTED', interim_state='AWAITING_SIGN_B')

    @transition(field=accept_state, source=STATUS_AWAITING_SIGN_B, target=STATUS_AWAITING_SIGN_C, permission=is_approver)
    def accept_sign_b(self):
        self.final_state = "ACCEPTED"
        self.interim_state = "AWAITING_SIGN_C"
        self.action = "ACCEPT_SIGN_B"
        ws = workflowitems.objects.get(id=self.id)
        workevents.objects.create(workitems=ws, from_state='AWAITING_SIGN_B',
                                  to_state='ACCEPTED', interim_state='AWAITING_SIGN_C')

    @transition(field=accept_state, source=STATUS_AWAITING_SIGN_C, target=STATUS_ACCEPTED, permission=is_approver)
    def accept_sign_c(self):
        self.final_state = "ACCEPTED"
        self.interim_state = "ACCEPTED"
        self.action = "ACCEPT_SIGN_C"
        ws = workflowitems.objects.get(id=self.id)
        workevents.objects.create(workitems=ws, from_state='AWAITING_SIGN_C',
                                  to_state='ACCEPTED', interim_state='ACCEPTED')

    # /-- ACTION : RETURN  --/

    @transition(field=accept_state, source=STATUS_AWAITING_SIGN_C, target=STATUS_AWAITING_SIGN_B)
    def return_1(self):
        self.interim_state = "AWAITING_SIGN_B"
        self.final_state = "AWAITING_SIGN_B"
        self.action = "RETURN"
        ws = workflowitems.objects.get(id=self.id)
        workevents.objects.create(workitems=ws, from_state='AWAITING_SIGN_C',
                                  to_state='AWAITING_SIGN_B', interim_state='AWAITING_SIGN_B')

    @transition(field=accept_state, source=STATUS_AWAITING_SIGN_B, target=STATUS_AWAITING_SIGN_A)
    def return_2(self):
        self.interim_state = "AWAITING_SIGN_A"
        self.final_state = "AWAITING_SIGN_A"
        self.action = "RETURN"
        ws = workflowitems.objects.get(id=self.id)
        workevents.objects.create(workitems=ws, from_state='AWAITING_SIGN_B',
                                  to_state='AWAITING_SIGN_A', interim_state='AWAITING_SIGN_A')

    @transition(field=accept_state, source=STATUS_AWAITING_SIGN_A, target=STATUS_DRAFT)
    def return_3(self):
        self.interim_state = "DRAFT"
        self.final_state = "DRAFT"
        self.action = "RETURN"
        ws = workflowitems.objects.get(id=self.id)
        workevents.objects.create(workitems=ws, from_state='AWAITING_SIGN_A',
                                  to_state='DRAFT', interim_state='DRAFT')
#   -----------------------------------------------------------------------------------------------------------------------------------

    # END OF TRANSITION'S

# -----------------------------------------------------------------------------------------------------------------------------------


# INVOICES MODEL

class Invoices(models.Model):

    finance_request_type = [
        ('AUTOMATIC', 'AUTOMATIC'),
        ('ON_REQUEST', 'ON_REQUEST')
    ]

    interest_choices = [
        ('FIXED', 'FIXED'),
        ('FLOATING', 'FLOATING')
    ]

    interest_rate_type_choices = [
        ('LIBOR', 'LIBOR'),
        ('EURIBOR', 'EURIBOR'),
        ('SOFOR', 'SOFOR')
    ]

    pairing = models.ForeignKey(Pairings, on_delete=models.DO_NOTHING)
    invoice_no = models.CharField(null=True, blank=True, max_length=10)
    issue_date = models.DateField(default=date.today)
    due_date = models.DateField(default=date.today)
    invoice_currency = models.ForeignKey(
        "accounts.Currencies", on_delete=models.CASCADE, related_name='invoicecurrencytype')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    funding_req_type = models.CharField(
        choices=finance_request_type, default=None, max_length=15)
    finance_currency_type = models.ForeignKey(
        "accounts.Currencies", on_delete=models.DO_NOTHING, related_name='financedinvoicecurrency')
    settlement_currency_type = models.ForeignKey(
        "accounts.Currencies", on_delete=models.CASCADE)
    interest_rate = models.DecimalField(max_digits=6, decimal_places=1)
    financed_amount = models.DecimalField(max_digits=6, decimal_places=1)
    bank_load_id = models.CharField(max_length=55)
    wf_item_id = models.ForeignKey(workflowitems, on_delete=models.CASCADE)

    def __str__(self):
        return "%s - invoice no is %s " % (self.pairing, self.invoice_no)


# INVOICE UPLOADS

class invoice_uploads(models.Model):
    program_type = [
        ('*', '*'),
        ('APF', 'APF'),
        ('RF', 'RF'),
        ('DF', 'DF')
    ]
    program_type = models.CharField(
        choices=program_type, default='*', max_length=15)
    invoices = models.JSONField()
    wf_item_id = models.ForeignKey(workflowitems, on_delete=models.CASCADE)


# WORKEVENTS

class workevents(models.Model):

    workitems = models.ForeignKey(
        workflowitems, on_delete=models.CASCADE, related_name='workflowevent')
    # event_user = models.ForeignKey('accounts.customer',on_delete=models.CASCADE,related_name='customername')
    from_state = models.CharField(max_length=50, default='DRAFT')
    to_state = models.CharField(max_length=50, default='DRAFT')
    interim_state = models.CharField(max_length=50, default='DRAFT')
    from_party = models.ForeignKey(
        'accounts.Parties', on_delete=models.CASCADE, related_name='from_we_party')
    to_party = models.ForeignKey(
        'accounts.Parties', on_delete=models.CASCADE, related_name='to_wf_party')
    # record_datas = models.JSONField()
    created_date = models.DateTimeField(auto_now_add=True)
