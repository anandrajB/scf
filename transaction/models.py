from random import choices
from django.db import models
from datetime import date
from django.dispatch import receiver
from django_fsm import FSMField, transition
from transaction.permission import is_approver, is_uploader
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField

from transaction.states import StateChoices

#  MODELS RELATED TO TRANSACTION


class submodels(models.Model):
    description = models.CharField(max_length=35)
    api_route = models.CharField(max_length=55)

    def __str__(self):
        return self.description


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

    Final_Check = [
        ("YES", "Y"),
        ("NO", "N")
    ]

    created_date = models.DateTimeField(auto_now_add=True)
    program = models.OneToOneField(Programs, on_delete=models.CASCADE)
    stage = models.CharField(max_length=255, choices=StateChoices.choices)
    initial_state = models.CharField(
        max_length=50, default=StateChoices.STATUS_DRAFT)
    interim_state = models.CharField(
        max_length=50, default=StateChoices.STATUS_DRAFT)
    final_state = models.CharField(
        max_length=50, default=StateChoices.STATUS_DRAFT)
    next_available_transitions = ArrayField(models.CharField(
        max_length=500, blank=True, null=True), blank=True, null=True)
    event_users = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name='customername')
    current_from_party = models.ForeignKey(
        "accounts.Parties", on_delete=models.DO_NOTHING, related_name='from_party')
    current_to_party = models.ForeignKey(
        "accounts.Parties", on_delete=models.DO_NOTHING, related_name='to_party')
    action = models.CharField(max_length=25, default='SAVE')
    final = models.CharField(choices=Final_Check, max_length=25, null=True, blank=True)
    # sign = models.ForeignKey('accounts.signatures',on_delete=models.CASCADE)


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
