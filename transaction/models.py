from django.db import models 
from django.db.models import Q
from datetime import date
from django.contrib.postgres.fields import ArrayField
from transaction.states import StateChoices



## FILE PATH DIRECTORY  -- ATTACHEMENT FILES -- 

def program_file_path(instance,filename):
    return 'scf/program/{0}/{1}'.format(instance.party.name , filename)


def pairing_file_path(instance,filename):
    return 'scf/pairing/user_{0}/{1}/{2}'.format(instance.counterparty_id.id , instance.counterparty_id.name , filename)


def invoice_upload_file_path(instance,filename):
    return 'scf/invoice_attachements/{0}'.format(filename)



#  MODELS RELATED TO TRANSACTION

class Transitionpartytype(models.Model):
    description = models.CharField(max_length=55)
    
    class Meta:
        verbose_name_plural = "Transitionpartytype"


class InterestRateType(models.Model):
    description = models.CharField(max_length=55)

    def __str__(self):
        return self.description
    
    def save(self, *args, **kwargs):
        self.description = self.description.upper()
        return super(InterestRateType, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "InterestRateType"



class InterestChoice(models.Model):
    description = models.CharField(max_length=55)

    def __str__(self):
        return self.description
    
    def save(self, *args, **kwargs):
        self.description = self.description.upper()
        return super(InterestChoice, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "InterestChoice"


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
    program_type = models.CharField(choices=program_type, default='*', max_length=10)
    finance_request_type = models.CharField(choices=finance_request_type, max_length=15, default=None,blank=True, null=True)
    limit_currency = models.CharField(max_length=3,blank=True, null=True)
    total_limit_amount = models.DecimalField(max_digits=8, decimal_places=2,blank=True, null=True)
    finance_currency = models.CharField(max_length=3,blank=True, null=True)
    settlement_currency = models.CharField(max_length=3,blank=True, null=True)
    expiry_date = models.DateField(default=date.today)
    max_finance_percentage = models.DecimalField(max_digits=8, decimal_places=2,blank=True, null=True)
    max_invoice_age_for_funding = models.IntegerField(blank=True, null=True)
    max_age_for_repayment = models.IntegerField(blank=True, null=True)
    minimum_period = models.IntegerField(blank=True, null=True)
    maximum_period = models.IntegerField(blank=True, null=True)
    maximum_amount = models.DecimalField(max_digits=8, decimal_places=2,blank=True, null=True)
    minimum_amount = models.DecimalField(max_digits=8, decimal_places=2,blank=True, null=True)
    financed_amount = models.DecimalField(max_digits=8, decimal_places=2,blank=True, null=True)
    balance_amount = models.DecimalField(max_digits=8, decimal_places=2,blank=True, null=True)
    grace_period = models.IntegerField(blank=True, null=True)
    attached_file = models.FileField(upload_to=program_file_path)
    interest_type = models.CharField(choices=interest_choices, default=None, max_length=15,blank=True, null=True)
    interest_rate_type = models.CharField(choices=interest_rate_type_choices, max_length=15, default=None,blank=True, null=True)
    interest_rate = models.DecimalField(max_digits=8, decimal_places=2,blank=True, null=True)
    margin = models.DecimalField(max_digits=8, decimal_places=2,blank=True, null=True)
    comments = models.CharField(max_length=155,blank=True, null=True)
    status = models.CharField(max_length=155,blank=True, null=True)
    is_locked = models.BooleanField(default=None,blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "Program"


# FUNDING REQUEST MODEL

class FundingRequest(models.Model):
    program = models.ForeignKey(Programs, on_delete=models.CASCADE)
    total_amount = models.IntegerField()
    financed_amount = models.DecimalField(max_digits=8, decimal_places=2)
    balance_amount = models.DecimalField(max_digits=8, decimal_places=2)
    due_date = models.DateField(default=date.today)

    def __str__(self):
        return "%s - %s -%s  due date of %s" % (self.program, self.total_amount, self.financed_amount, self.financed_amount)

    class Meta:
        verbose_name_plural = "FundingRequest"


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

    program_id = models.ForeignKey(Programs, on_delete=models.CASCADE)
    counterparty_id = models.OneToOneField("accounts.Parties", on_delete=models.CASCADE)
    finance_request = models.CharField(choices=finance_request_type, max_length=15, default=None,blank=True, null=True)
    currency = models.ForeignKey("accounts.Currencies", on_delete=models.DO_NOTHING, related_name='pairingscurrency',blank=True, null=True)
    total_limit = models.DecimalField(max_digits=8, decimal_places=2,blank=True, null=True)
    finance_currency_type = models.ForeignKey("accounts.Currencies", on_delete=models.DO_NOTHING, related_name='financedcurrency',blank=True, null=True)
    settlement_currency_type = models.ForeignKey("accounts.Currencies", on_delete=models.CASCADE,blank=True, null=True)
    expiry_date = models.DateField(default=date.today)
    max_finance_percentage = models.DecimalField(max_digits=8, decimal_places=2,blank=True, null=True)
    max_invoice_age_for_funding = models.IntegerField(blank=True, null=True)
    max_age_for_repayment = models.IntegerField(blank=True, null=True)
    minimum_period = models.IntegerField(blank=True, null=True)
    maximum_period = models.IntegerField(blank=True, null=True)
    minimum_amount_currency = models.CharField(max_length=3,blank=True, null=True)
    minimum_amount = models.DecimalField(max_digits=8, decimal_places=2,blank=True, null=True)
    maximum_amount = models.DecimalField(max_digits=8, decimal_places=2,blank=True, null=True)
    financed_amount = models.DecimalField(max_digits=8, decimal_places=2,blank=True, null=True)
    balance_amount = models.DecimalField(max_digits=8, decimal_places=2,blank=True, null=True)
    grace_period = models.IntegerField(blank=True, null=True)
    attached_file = models.FileField(upload_to=pairing_file_path)
    interest_type = models.CharField(choices=interest_choices, default=None, max_length=15,blank=True, null=True)
    interest_rate_type = models.CharField(choices=interest_rate_type_choices, max_length=15, default=None)
    interest_rate = models.DecimalField(max_digits=8, decimal_places=2,blank=True, null=True)
    margin = models.DecimalField(max_digits=8, decimal_places=2,blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Pairing"

    



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
    
    party = models.ForeignKey("accounts.Parties", on_delete=models.CASCADE,blank=True, null=True)
    program_type = models.CharField(max_length=255,blank=True, null=True)
    pairing = models.ForeignKey(Pairings, on_delete=models.DO_NOTHING,blank=True, null=True)
    invoice_no = models.CharField(null=True, blank=True, max_length=10)
    issue_date = models.DateField(default=date.today,blank=True, null=True)
    due_date = models.DateField(default=date.today,blank=True, null=True)
    invoice_currency = models.ForeignKey("accounts.Currencies", on_delete=models.CASCADE, related_name='invoicecurrencytype',blank=True, null=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2,blank=True, null=True)
    funding_req_type = models.CharField(choices=finance_request_type, default=None, max_length=15,blank=True, null=True)
    finance_currency_type = models.ForeignKey("accounts.Currencies", on_delete=models.DO_NOTHING, related_name='financedinvoicecurrency',blank=True, null=True)
    settlement_currency_type = models.ForeignKey("accounts.Currencies", on_delete=models.CASCADE,blank=True, null=True)
    interest_rate = models.DecimalField(max_digits=8, decimal_places=1,blank=True, null=True)
    financed_amount = models.DecimalField(max_digits=8, decimal_places=1,blank=True, null=True)
    bank_loan_id = models.CharField(max_length=55,blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        verbose_name_plural = "Invoice"


# INVOICE UPLOADS

class Invoiceuploads(models.Model):
    program_type = [
        ('*', '*'),
        ('APF', 'APF'),
        ('RF', 'RF'),
        ('DF', 'DF')
    ]
    program_type = models.CharField(choices=program_type, default='*', max_length=15)
    # user = models.OneToOneField("accounts.User", on_delete=models.CASCADE, related_name='customername')
    invoices = models.JSONField()
    attached_file = models.FileField(upload_to=invoice_upload_file_path)
    is_finished = models.BooleanField(default=None,blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Invoiceupload"




# WORKFLOW ITEMS MODEL

class workflowitems(models.Model):
    
    created_date = models.DateTimeField(auto_now_add=True)
    program = models.OneToOneField(Programs, on_delete=models.CASCADE,blank=True, null=True)
    invoice = models.OneToOneField(Invoices,on_delete=models.CASCADE,blank=True, null=True)
    uploads = models.OneToOneField(Invoiceuploads,on_delete=models.CASCADE,blank=True, null=True)
    initial_state = models.CharField(max_length=50, default=StateChoices.STATUS_DRAFT)
    interim_state = models.CharField(max_length=50, default=StateChoices.STATUS_DRAFT)
    final_state = models.CharField(max_length=50, default=StateChoices.STATUS_DRAFT)
    next_available_transitions = ArrayField(models.CharField(max_length=500,blank=True, null=True,default=None),blank=True, null=True,default = None)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name='customername')
    current_from_party = models.ForeignKey("accounts.Parties", on_delete=models.DO_NOTHING, related_name='from_party')
    current_to_party = models.ForeignKey("accounts.Parties", on_delete=models.DO_NOTHING, related_name='to_party')
    action = models.CharField(max_length=25, default='SAVE')
    subaction = models.CharField(max_length=55 , blank=True, null=True)
    type = models.CharField(max_length=55)
    is_read = models.BooleanField(default=True,blank=True, null=True)

    class Meta:
        verbose_name_plural = "Workflowitem"

        

# WORKEVENTS
class workevents(models.Model):

    workitems = models.ForeignKey(workflowitems, on_delete=models.CASCADE, related_name='workflowevent')
    from_state = models.CharField(max_length=50, default='DRAFT')
    action = models.CharField(max_length=25, default='SAVE')
    subaction = models.CharField(max_length=55 , blank=True, null=True)
    to_state = models.CharField(max_length=50, default='DRAFT')
    interim_state = models.CharField(max_length=50, default='DRAFT')
    from_party = models.ForeignKey('accounts.Parties', on_delete=models.CASCADE, related_name='from_we_party')
    to_party = models.ForeignKey('accounts.Parties', on_delete=models.CASCADE, related_name='to_wf_party')
    event_user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='event_user')
    record_datas = models.JSONField(blank=True, null=True)
    end = models.CharField(max_length=55,blank=True, null=True)
    is_read = models.BooleanField(default=True,blank=True, null=True)
    final = models.CharField(max_length=55,blank=True, null=True)
    c_final = models.CharField(max_length=55,blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=55)
    
    class Meta:
        verbose_name_plural = "WorkEvent"
        ordering = ['id']

    # def save(self, *args, **kwargs):
    #     program = Programs.objects.filter(id=self.workitems.program.id).values()
    #     jsoni = json.dumps(list(program),sort_keys = True,default = None, use_decimal = True)
    #     print(jsoni)
    #     self.record_datas = "anand"
    #     return super(workevents, self).save(*args, **kwargs)

    
    def save(self, *args, **kwargs):
        try:
            qs = Programs.objects.get(id =self.workitems.program.id)
            # qs2 = Programs.objects.get(id = self.workitems.invoice.pairing.program_id.id)
            # qs1 = Invoices.objects.get(id = self.workitems.invoices)
            # qs2 = Invoiceuploads.objects.get(id = self.workitems.uploads)
            program_data_template = {
                    "party" : qs.party.name,
                    "party_type" : qs.party.party_type,
                    "program_type" : qs.program_type,
                    "finance_request_type" : qs.finance_request_type,
                    "limit_currency": qs.limit_currency,
                    "total_limit_amount":str(qs.total_limit_amount),
                    "finance_currency" : qs.finance_currency,
                    "settlement_currency" : qs.settlement_currency,
                    # "expiry_date" : qs.expiry_date,
                    "max_finance_percentage":str(qs.max_finance_percentage),
                    "max_invoice_age_for_funding" : qs.max_invoice_age_for_funding,
                    "max_age_for_repayment" : qs.max_age_for_repayment,
                    "minimum_period" : qs.minimum_period,
                    "maximum_period" : str(qs.maximum_period),
                    "maximum_amount" : str(qs.maximum_amount),
                    "minimum_amount" : str(qs.minimum_amount),
                    "financed_amount":str(qs.financed_amount),
                    "balance_amount" : str(qs.balance_amount),
                    "grace_period" : qs.grace_period,
                    "interest_type" : qs.interest_type,
                    "interest_rate_type" : qs.interest_rate_type,
                    "interest_rate": str(qs.interest_rate),
                    "margin" : str(qs.margin),
                    "status" : qs.status,
                    "is_locked" : qs.is_locked,
                    # "created_date" : qs.created_date
            }
            # invoice_data_template = {
            #     "party" : qs1.party.name,
            #     "party_type" : qs1.party.party_type,
            #     "program_type" : qs1.program_type,
            #     "pairing":qs1.pairing,
            #     "invoice_no":qs1.invoice_no,
            #     "issue_date":qs1.issue_date,
            #     "due_date":qs1.due_date,
            #     "invoice_currency":qs1.invoice_currency,
            #     "amount":qs1.amount,
            #     "funding_req_type":qs1.funding_req_type,
            #     "finance_currency_type" :qs1.finance_currency_type,
            #     "settlement_currency_type" :qs1.settlement_currency_type,
            #     "interest_rate" : qs1.interest_rate,
            #     "financed_amount" : qs1.financed_amount,
            #     "bank_loan_id" : qs1.bank_loan_id,
            #     "created_date" : qs1.created_date
            # }
            self.record_datas = program_data_template
            return super(workevents, self).save( *args, **kwargs) 
        except:
            self.record_datas = None
            return super(workevents, self).save( *args, **kwargs)
    
        
