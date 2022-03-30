from django.db import models
from datetime import date
from django.contrib.postgres.fields import ArrayField
from transaction.states import StateChoices


#  MODELS RELATED TO TRANSACTION

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
        choices=finance_request_type, max_length=15, default=None, blank=True, null=True)
    limit_currency = models.CharField(max_length=3, blank=True, null=True)
    total_limit_amount = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    finance_currency = models.CharField(max_length=3, blank=True, null=True)
    settlement_currency = models.CharField(max_length=3, blank=True, null=True)
    expiry_date = models.DateField(default=date.today)
    max_finance_percentage = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    max_invoice_age_for_funding = models.IntegerField(blank=True, null=True)
    max_age_for_repayment = models.IntegerField(blank=True, null=True)
    minimum_period = models.IntegerField(blank=True, null=True)
    maximum_period = models.IntegerField(blank=True, null=True)
    maximum_amount = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    minimum_amount = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    financed_amount = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    balance_amount = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    grace_period = models.IntegerField(blank=True, null=True)
    interest_type = models.CharField(
        choices=interest_choices, default=None, max_length=15, blank=True, null=True)
    interest_rate_type = models.CharField(
        choices=interest_rate_type_choices, max_length=15, default=None, blank=True, null=True)
    interest_rate = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    margin = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    comments = models.CharField(max_length=155, blank=True, null=True)


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

    program_id = models.ForeignKey(Programs, on_delete=models.DO_NOTHING)
    counterparty_id = models.OneToOneField(
        "accounts.Parties", on_delete=models.CASCADE)
    finance_request = models.CharField(
        choices=finance_request_type, max_length=15, default=None, blank=True, null=True)
    currency = models.ForeignKey("accounts.Currencies", on_delete=models.DO_NOTHING,
                                 related_name='pairingscurrency', blank=True, null=True)
    total_limit = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    finance_currency_type = models.ForeignKey(
        "accounts.Currencies", on_delete=models.DO_NOTHING, related_name='financedcurrency', blank=True, null=True)
    settlement_currency_type = models.ForeignKey(
        "accounts.Currencies", on_delete=models.CASCADE, blank=True, null=True)
    expiry_date = models.DateField(default=date.today)
    max_finance_percentage = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    max_invoice_age_for_funding = models.IntegerField(blank=True, null=True)
    max_age_for_repayment = models.IntegerField(blank=True, null=True)
    minimum_period = models.IntegerField(blank=True, null=True)
    maximum_period = models.IntegerField(blank=True, null=True)
    minimum_amount_currency = models.CharField(
        max_length=3, blank=True, null=True)
    minimum_amount = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    maximum_amount = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    financed_amount = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    balance_amount = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    grace_period = models.IntegerField(blank=True, null=True)
    interest_type = models.CharField(
        choices=interest_choices, default=None, max_length=15, blank=True, null=True)
    interest_rate_type = models.CharField(
        choices=interest_rate_type_choices, max_length=15, default=None)
    interest_rate = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    margin = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)


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

    party = models.ForeignKey(
        "accounts.Parties", on_delete=models.CASCADE, blank=True, null=True)
    program_type = models.CharField(max_length=255, blank=True, null=True)
    pairing = models.ForeignKey(
        Pairings, on_delete=models.DO_NOTHING, blank=True, null=True)
    invoice_no = models.CharField(null=True, blank=True, max_length=10)
    issue_date = models.DateField(default=date.today, blank=True, null=True)
    due_date = models.DateField(default=date.today, blank=True, null=True)
    invoice_currency = models.ForeignKey(
        "accounts.Currencies", on_delete=models.CASCADE, related_name='invoicecurrencytype', blank=True, null=True)
    amount = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    funding_req_type = models.CharField(
        choices=finance_request_type, default=None, max_length=15, blank=True, null=True)
    finance_currency_type = models.ForeignKey(
        "accounts.Currencies", on_delete=models.DO_NOTHING, related_name='financedinvoicecurrency', blank=True, null=True)
    settlement_currency_type = models.ForeignKey(
        "accounts.Currencies", on_delete=models.CASCADE, blank=True, null=True)
    interest_rate = models.DecimalField(
        max_digits=8, decimal_places=1, blank=True, null=True)
    financed_amount = models.DecimalField(
        max_digits=8, decimal_places=1, blank=True, null=True)
    bank_loan_id = models.CharField(max_length=55, blank=True, null=True)


# INVOICE UPLOADS

class Invoiceuploads(models.Model):
    program_type = [
        ('*', '*'),
        ('APF', 'APF'),
        ('RF', 'RF'),
        ('DF', 'DF')
    ]
    program_type = models.CharField(
        choices=program_type, default='*', max_length=15)
    invoices = models.JSONField()


# WORKFLOW ITEMS MODEL

class workflowitems(models.Model):

    created_date = models.DateTimeField(auto_now_add=True)
    program = models.OneToOneField(
        Programs, on_delete=models.CASCADE, blank=True, null=True)
    invoice = models.OneToOneField(
        Invoices, on_delete=models.CASCADE, blank=True, null=True)
    uploads = models.OneToOneField(
        Invoiceuploads, on_delete=models.CASCADE, blank=True, null=True)
    initial_state = models.CharField(
        max_length=50, default=StateChoices.STATUS_DRAFT)
    interim_state = models.CharField(
        max_length=50, default=StateChoices.STATUS_DRAFT)
    final_state = models.CharField(
        max_length=50, default=StateChoices.STATUS_DRAFT)
    next_available_transitions = ArrayField(models.CharField(
        max_length=500, blank=True, null=True), blank=True, null=True)
    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name='customername')
    current_from_party = models.ForeignKey(
        "accounts.Parties", on_delete=models.DO_NOTHING, related_name='from_party')
    current_to_party = models.ForeignKey(
        "accounts.Parties", on_delete=models.DO_NOTHING, related_name='to_party')
    action = models.CharField(max_length=25, default='SAVE')
    subaction = models.CharField(max_length=55, blank=True, null=True)
    event = models.ForeignKey(
        'workevents', on_delete=models.CASCADE, blank=True, null=True)
    flow_field = models.CharField(
        max_length=255, default=StateChoices.STATUS_DRAFT)


# WORKEVENTS

class workevents(models.Model):

    workitems = models.ForeignKey(
        workflowitems, on_delete=models.CASCADE, related_name='workflowevent')
    from_state = models.CharField(max_length=50, default='DRAFT')
    to_state = models.CharField(max_length=50, default='DRAFT')
    interim_state = models.CharField(max_length=50, default='DRAFT')
    from_party = models.ForeignKey(
        'accounts.Parties', on_delete=models.CASCADE, related_name='from_we_party')
    to_party = models.ForeignKey(
        'accounts.Parties', on_delete=models.CASCADE, related_name='to_wf_party')
    event_user = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE, related_name='event_user')
    record_datas = models.JSONField(blank=True, null=True)
    end = models.CharField(max_length=55, blank=True, null=True)
    final = models.CharField(max_length=55, blank=True, null=True)
    c_final = models.CharField(max_length=55, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=55)
    b_final = models.CharField(max_length=55, blank=True, null=True)
    s_final = models.CharField(max_length=55, blank=True, null=True)
