from distutils.command.upload import upload
from email.policy import default
from urllib import request
from rest_framework import serializers
from .models import Invoices, Invoiceuploads, Pairings, Programs, workflowitems
from accounts.models import Currencies, User, signatures,  Parties, userprocessauth
from .models import workevents
from django.contrib.auth import get_user_model

User = get_user_model()





class PairingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pairings
        fields = '__all__'


# WORKEVENTS SERIALIZER

class Workeventsserializer(serializers.ModelSerializer):
    from_party = serializers.SlugRelatedField(read_only=True, slug_field='name')
    to_party = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = workevents
        fields = [
            'workitems',
            'from_state',
            'to_state',
            'interim_state',
            'from_party',
            'to_party',
            'created_date'
        ]



#   WORK EVENT FOR MESSAGE SERIALIZER ( INBOX - BANK)

class Workeventsmessageserializer(serializers.ModelSerializer):
    from_party = serializers.SlugRelatedField(read_only=True, slug_field='name')
    to_party = serializers.SlugRelatedField(read_only=True, slug_field='name')
    program = serializers.PrimaryKeyRelatedField(queryset = workflowitems.objects.all() , source = 'workitems')
    action = serializers.SerializerMethodField()
    subaction = serializers.SerializerMethodField()

    class Meta:
        model = workevents
        fields = [
            'program',
            'from_state',
            'to_state',
            'interim_state',
            'from_party',
            'to_party',
            'action',
            'subaction',
            'created_date'
        ]

    def get_action(self,obj):
        return obj.workitems.action

    def get_subaction(self,obj):
        return obj.workitems.subaction


# WORKFLOW-ITEMS SERIALIZER

class Workitemserializer(serializers.ModelSerializer):
    workflowevent = Workeventsserializer(many=True, read_only=True)
    current_from_party = serializers.SlugRelatedField(read_only=True, slug_field='name')
    current_to_party = serializers.SlugRelatedField(read_only=True, slug_field='name')
    wf_item_id = serializers.SerializerMethodField()

    class Meta:
        model = workflowitems
        fields = [
            'wf_item_id',
            'initial_state',
            'interim_state',
            'final_state',
            'next_available_transitions',
            'current_from_party',
            'current_to_party',
            'event_users',
            'created_date',
            'action',
            'subaction',
            'workflowevent'

        ]
        read_only_fields = ['workflowevent']

    def get_wf_item_id(self,obj):
        return obj.id



# PROGRAM SERIALIZER

class ProgramListserializer(serializers.ModelSerializer):
    workflowitems = Workitemserializer(read_only=True)
    workevents = Workeventsserializer(read_only=True)
    party = serializers.SlugRelatedField(read_only=True, slug_field='name')
    created_by = serializers.SerializerMethodField()
    wf_item_id = serializers.SerializerMethodField()

    class Meta:
        model = Programs
        fields = [
            "id",
            "wf_item_id",
            "party",
            'created_by',
            "program_type",
            "finance_request_type",
            "limit_currency",
            "total_limit_amount",
            "finance_currency",
            "settlement_currency",
            "expiry_date",
            "max_finance_percentage",
            'max_invoice_age_for_funding',
            "max_age_for_repayment",
            "minimum_period",
            "maximum_period",
            "maximum_amount",
            "minimum_amount",
            "financed_amount",
            "grace_period",
            "interest_type",
            'interest_rate_type',
            'interest_rate',
            'margin',
            'workflowitems',
            'workevents',
        ]

    def get_created_by(self,obj):
        return obj.workflowitems.event_users.email

    def get_wf_item_id(self,obj):
        return obj.workflowitems.id




# PROGRAM CREATE SERIALIZER

class Programcreateserializer(serializers.Serializer):

    def current_user(request):
        return request.user.id

    finance_request_type = [
        ('AUTOMATIC', 'AUTOMATIC'),
        ('ON_REQUEST', 'ON_REQUEST')
    ]

    interest_type = [
        ('FIXED', 'FIXED'),
        ('FLOATING', 'FLOATING')
    ]

    interest_rate_type = [
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
    
    party = serializers.PrimaryKeyRelatedField(queryset=Parties.objects.all())
    program_type = serializers.ChoiceField(choices=program_type)
    finance_request_type = serializers.ChoiceField(choices=finance_request_type, default=None)
    limit_currency = serializers.CharField()
    total_limit_amount = serializers.DecimalField(max_digits=8, decimal_places=2)
    finance_currency = serializers.CharField()
    settlement_currency = serializers.CharField()
    expiry_date = serializers.DateField(format="%d-%m-%Y")
    max_finance_percentage = serializers.DecimalField(max_digits=8, decimal_places=2)
    max_invoice_age_for_funding = serializers.IntegerField()
    max_age_for_repayment = serializers.IntegerField()
    minimum_period = serializers.IntegerField()
    maximum_period = serializers.IntegerField()
    maximum_amount = serializers.DecimalField(max_digits=8, decimal_places=2)
    minimum_amount = serializers.DecimalField(max_digits=8, decimal_places=2)
    financed_amount = serializers.DecimalField(max_digits=8, decimal_places=2)
    balance_amount = serializers.DecimalField(max_digits=8, decimal_places=2)
    grace_period = serializers.IntegerField()
    interest_type = serializers.ChoiceField(choices=interest_type)
    interest_rate_type = serializers.ChoiceField(choices=interest_rate_type)
    interest_rate = serializers.DecimalField(max_digits=8, decimal_places=2)
    margin = serializers.DecimalField(max_digits=8, decimal_places=2)
    event_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    # sign = serializers.PrimaryKeyRelatedField(queryset = signatures.objects.all())
    # record_datas = serializers.JSONField()
    from_party = serializers.PrimaryKeyRelatedField(queryset=Parties.objects.all())
    to_party = serializers.PrimaryKeyRelatedField(queryset=Parties.objects.all())

    def create(self, validated_data):
        party = validated_data.pop('party')
        program_type = validated_data.pop('program_type')
        finance_request_type = validated_data.pop('finance_request_type')
        limit_currency = validated_data.pop('limit_currency')
        total_limit_amount = validated_data.pop('total_limit_amount')
        finance_currency = validated_data.pop('finance_currency')
        settlement_currency = validated_data.pop('settlement_currency')
        expiry_date = validated_data.pop('expiry_date')
        max_finance_percentage = validated_data.pop('max_finance_percentage')
        max_invoice_age_for_funding = validated_data.pop('max_invoice_age_for_funding')
        max_age_for_repayment = validated_data.pop('max_age_for_repayment')
        minimum_period = validated_data.pop('minimum_period')
        maximum_period = validated_data.pop('maximum_period')
        maximum_amount = validated_data.pop('maximum_amount')
        minimum_amount = validated_data.pop('minimum_amount')
        financed_amount = validated_data.pop('financed_amount')
        balance_amount = validated_data.pop('balance_amount')
        grace_period = validated_data.pop('grace_period')
        from_party = validated_data.pop('from_party')
        to_party = validated_data.pop('to_party')
        interest_type = validated_data.pop('interest_type')
        interest_rate_type = validated_data.pop('interest_rate_type')
        interest_rate = validated_data.pop('interest_rate')
        margin = validated_data.pop('margin')
        event_user = validated_data.pop('event_user')
        # sign = validated_data.pop('sign')
        # record_datas = validated_data.pop('record_datas')

        program = Programs.objects.create(
            party=party, program_type=program_type, finance_request_type=finance_request_type,
            limit_currency=limit_currency, total_limit_amount=total_limit_amount, finance_currency=finance_currency,
            settlement_currency=settlement_currency, expiry_date=expiry_date, max_finance_percentage=max_finance_percentage,
            max_invoice_age_for_funding=max_invoice_age_for_funding, max_age_for_repayment=max_age_for_repayment,
            minimum_amount=minimum_amount, minimum_period=minimum_period, maximum_amount=maximum_amount,
            maximum_period=maximum_period, financed_amount=financed_amount, balance_amount=balance_amount,
            grace_period=grace_period, interest_rate=interest_rate, interest_rate_type=interest_rate_type,
            interest_type=interest_type, margin=margin 
        )
        program.save()
        work = workflowitems.objects.create(
            program=program, current_from_party=from_party,current_to_party=to_party, event_users=event_user)
        work.save()
        event = workevents.objects.create(
            workitems=work, from_party=from_party, to_party=to_party)
        event.save()
        return program





#------------------------------------------------------

# INVOICE SERIALIZER SETUP

#------------------------------------------------------



# INVOICE CREATE SERIALIZER 

class InvoiceCreateserializer(serializers.Serializer):
    finance_request_type = [
        ('AUTOMATIC', 'AUTOMATIC'),
        ('ON_REQUEST', 'ON_REQUEST')
    ]

    party = serializers.PrimaryKeyRelatedField(queryset=Parties.objects.all())
    pairing = serializers.PrimaryKeyRelatedField(queryset = Pairings.objects.all())
    invoice_number = serializers.CharField()
    issue_date = serializers.DateField(format="%d-%m-%Y")
    due_date = serializers.DateField(format="%d-%m-%Y")
    invoice_currency = serializers.PrimaryKeyRelatedField(queryset = Currencies.objects.all())
    amount = serializers.DecimalField(max_digits=8, decimal_places=2)
    funding_request_type = serializers.ChoiceField(choices = finance_request_type,default = None)
    finance_currency_type =  serializers.PrimaryKeyRelatedField(queryset = Currencies.objects.all())
    settlement_currency_type = serializers.PrimaryKeyRelatedField(queryset = Currencies.objects.all())
    interest_rate = serializers.DecimalField(max_digits=8, decimal_places=2)
    financed_amount = serializers.DecimalField(max_digits=8, decimal_places=2)
    bank_loan_id = serializers.CharField()
    event_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    # sign = serializers.PrimaryKeyRelatedField(queryset = signatures.objects.all())
    # record_datas = serializers.JSONField()
    from_party = serializers.PrimaryKeyRelatedField(queryset=Parties.objects.all())
    to_party = serializers.PrimaryKeyRelatedField(queryset=Parties.objects.all())
    
    def create(self, validated_data):
        pairing = validated_data.pop('pairing')
        party = validated_data.pop('party')
        invoice_number = validated_data.pop('invoice_number')
        issue_date = validated_data.pop('issue_date')
        due_date = validated_data.pop('due_date')
        invoice_currency = validated_data.pop('invoice_currency')
        amount = validated_data.pop('amount')
        funding_request_type = validated_data.pop('funding_request_type')
        finance_currency_type = validated_data.pop('finance_currency_type')
        settlement_currency_type = validated_data.pop('settlement_currency_type')
        interest_rate = validated_data.pop('interest_rate')
        financed_amount = validated_data.pop('financed_amount')
        bank_loan = validated_data.pop('bank_loan_id')
        from_party = validated_data.pop('from_party')
        to_party = validated_data.pop('to_party')
        event_user = validated_data.pop('event_user')
        invoice = Invoices.objects.create(party = party,pairing = pairing , invoice_no =  invoice_number , issue_date = issue_date ,due_date = due_date , invoice_currency = invoice_currency,amount = amount,funding_req_type = funding_request_type,finance_currency_type = finance_currency_type,settlement_currency_type = settlement_currency_type , interest_rate = interest_rate , financed_amount = financed_amount , bank_loan_id = bank_loan )
        invoice.save()
        work = workflowitems.objects.create(
            invoice=invoice, current_from_party=from_party,current_to_party=to_party, event_users=event_user)
        work.save()
        event = workevents.objects.create(
            workitems=work, from_party=from_party, to_party=to_party)
        event.save()
        return invoice


class WorkeventInvoicesserializer(serializers.ModelSerializer):
    from_party = serializers.SlugRelatedField(read_only=True, slug_field='name')
    to_party = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = workevents
        fields = [
            'workitems',
            'from_state',
            'to_state',
            'interim_state',
            'from_party',
            'to_party',
            'final',
            'created_date'
        ]


class WorkitemInvoiceserializer(serializers.ModelSerializer):
    workflowevent = WorkeventInvoicesserializer(many=True, read_only=True)
    current_from_party = serializers.SlugRelatedField(read_only=True, slug_field='name')
    current_to_party = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = workflowitems
        fields = [
            'invoice',
            'initial_state',
            'interim_state',
            'final_state',
            'next_available_transitions',
            'current_from_party',
            'current_to_party',
            'event_users',
            'created_date',
            'action',
            'subaction',
            'workflowevent'

        ]
        read_only_fields = ['workflowevent']


class InvoiceSerializer(serializers.ModelSerializer):
    workflowitems = WorkitemInvoiceserializer(read_only=True)
    workevents = WorkeventInvoicesserializer(read_only=True)
    party = serializers.SlugRelatedField(read_only=True, slug_field='name')
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Invoices
        fields = [
            'id',
            'party',
            'created_by',
            'pairing',
            'invoice_no',
            'issue_date',
            'due_date',
            'invoice_currency',
            'amount',
            'funding_req_type',
            'finance_currency_type',
            'settlement_currency_type',
            'interest_rate',
            'financed_amount',
            'bank_loan_id',
            'workflowitems',
            'workevents'
        ]
    

    def get_created_by(self,obj):
        return obj.workflowitems.event_users.email




#--------------------------------------

# INVOICE UPLOAD  SERIALIZER SETUP

#-------------------------------------

class InvoiceUploadserializer(serializers.Serializer):
    program_type = [
        ('*', '*'),
        ('APF', 'APF'),
        ('RF', 'RF'),
        ('DF', 'DF')
    ]

    program_type = serializers.ChoiceField(choices = program_type)
    buyer_id = serializers.IntegerField()
    buyer_name = serializers.CharField()
    invoice_no = serializers.IntegerField()
    invoice_date = serializers.DateField(format="%d/%m/%Y")
    invoice_amount = serializers.IntegerField()
    due_date = serializers.DateField(format="%d/%m/%Y")
    financing_currency = serializers.PrimaryKeyRelatedField(queryset = Currencies.objects.all())
    settlement_currency = serializers.PrimaryKeyRelatedField(queryset = Currencies.objects.all())
    event_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    from_party = serializers.PrimaryKeyRelatedField(queryset=Parties.objects.all())
    to_party = serializers.PrimaryKeyRelatedField(queryset=Parties.objects.all())


    def create(self, validated_data):
        program_type = validated_data.pop('program_type')
        buyer_id = validated_data.pop('buyer_id')
        buyer_name = validated_data.pop('buyer_name')
        invoice_no = validated_data.pop('invoice_no')
        invoice_date = validated_data.pop('invoice_date')
        invoice_amount = validated_data.pop('invoice_amount')
        due_date = validated_data.pop('due_date')
        financing_currency = validated_data.pop('financing_currency')
        settlement_currency = validated_data.pop('settlement_currency')
        from_party = validated_data.pop('from_party')
        to_party = validated_data.pop('to_party')
        event_user = validated_data.pop('event_user')

        invoices = {
            'buyer_id' : buyer_id,
            'buyer_name' : buyer_name,
            'invoice_no' : invoice_no,
            'invoice_date' : str(invoice_date),
            'invoice_amount' : invoice_amount,
            'due_date' : str(due_date),
            'financing_currency' : str(financing_currency),
            'settlement_currency' : str(settlement_currency)
        }
        uploads = Invoiceuploads.objects.create(program_type = program_type , invoices = invoices ,**validated_data)
        work = workflowitems.objects.create(
            uploads=uploads, current_from_party=from_party,current_to_party=to_party, event_users=event_user)
        event = workevents.objects.create(
            workitems=work, from_party=from_party, to_party=to_party) 
        uploads.save()
        work.save()
        event.save()
        return uploads




class WorkeventInvoiceUploadsserializer(serializers.ModelSerializer):
    from_party = serializers.SlugRelatedField(read_only=True, slug_field='name')
    to_party = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = workevents
        fields = [
            'workitems',
            'from_state',
            'to_state',
            'interim_state',
            'from_party',
            'to_party',
            'final',
            'created_date'
        ]


class WorkitemInvoiceUploadserializer(serializers.ModelSerializer):
    workflowevent = WorkeventInvoiceUploadsserializer(many=True, read_only=True)
    current_from_party = serializers.SlugRelatedField(read_only=True, slug_field='name')
    current_to_party = serializers.SlugRelatedField(read_only=True, slug_field='name')
    wf_item_id = serializers.SerializerMethodField()
    class Meta:
        model = workflowitems
        fields = [
            'wf_item_id',
            'uploads',
            'initial_state',
            'interim_state',
            'final_state',
            'next_available_transitions',
            'current_from_party',
            'current_to_party',
            'event_users',
            'created_date',
            'action',
            'subaction',
            'workflowevent'

        ]
        read_only_fields = ['workflowevent']
    
    def get_wf_item_id(self,obj):
        return obj.id


class InvoiceUploadlistserializer(serializers.ModelSerializer):
    workflowitems = WorkitemInvoiceUploadserializer(read_only=True)
    workevents = WorkeventInvoiceUploadsserializer(read_only=True)
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Invoiceuploads
        fields = [
            'id',
            'program_type',
            'created_by',
            'invoices',
            'workflowitems',
            'workevents'
        ]
    

    def get_created_by(self,obj):
        return obj.workflowitems.event_users.email
