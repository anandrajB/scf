from distutils.command.upload import upload
from rest_framework import serializers
from .models import (
    Invoices,
    Invoiceuploads,
    Pairings,
    Programs,
    workflowitems
)
from accounts.models import (
    Countries, 
    Currencies, 
    User, 
    Parties, 
)
from .models import workevents
from django.contrib.auth import get_user_model

User = get_user_model()



# PAIRING LIST AND CREATE SERIALIZER 

class PairingSerializer(serializers.ModelSerializer):
    buyer_name = serializers.SerializerMethodField()
    program_user = serializers.SerializerMethodField()
    counterparty_id = serializers.SlugRelatedField(read_only=True, slug_field='name')
    city = serializers.SerializerMethodField()
    
    class Meta:
        model = Pairings
        fields = '__all__'
        read_only_fields = ['buyer_name','program_user']
        
    def get_buyer_name(self,obj):
        return obj.program_id.party.name

    def get_city(self,obj):
        return obj.counterparty_id.city

    def get_program_user(self,obj):
        return obj.program_id.workflowitems.user.display_name


#   WORK EVENT FOR MESSAGE SERIALIZER ( INBOX - BANK)

class Workeventsmessageserializer(serializers.ModelSerializer):
    from_party = serializers.SlugRelatedField(read_only=True, slug_field='name')
    to_party = serializers.SlugRelatedField(read_only=True, slug_field='name')
    wf_item_id = serializers.PrimaryKeyRelatedField(queryset = workflowitems.objects.all() , source = 'workitems')
    program = serializers.PrimaryKeyRelatedField(queryset = Programs.objects.all() , source = 'workitems.program')
    invoice = serializers.PrimaryKeyRelatedField(queryset = Invoices.objects.all() , source = 'workitems.invoice')
    invoice_upload = serializers.PrimaryKeyRelatedField(queryset = Invoiceuploads.objects.all() , source = 'workitems.uploads')
    status = serializers.SerializerMethodField()
    display_name = serializers.SerializerMethodField()
    record_datas = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = workevents
        fields = [
            'id',
            'wf_item_id',
            'type',
            'program',
            'invoice_upload',
            'invoice',
            'record_datas',
            'from_state',
            'to_state',
            'created_by',
            'interim_state',
            'from_party',
            'to_party',
            'event_user',
            'display_name',
            'status',
            'created_date'
        ]

    def get_created_by(self,obj):
        return obj.workitems.user.email

    def get_record_datas(self,obj):
        item_id = obj.workitems
        if obj.type == "PROGRAM":
            qs = Programs.objects.filter(workflowitems = item_id).values()
        elif obj.type == "INVOICE":
            qs = Invoices.objects.filter(workflowitems = item_id).values()
        elif obj.type == "UPLOAD":
            qs = Invoiceuploads.objects.filter(workflowitems = item_id).values()
        return qs

    def get_display_name(self,obj):
        return obj.event_user.display_name

    def get_status(self,obj):
        return obj.to_state


# WORKEVENTS SERIALIZER

class Workeventsserializer(serializers.ModelSerializer):
    from_party = serializers.SlugRelatedField(read_only=True, slug_field='name')
    to_party = serializers.SlugRelatedField(read_only=True, slug_field='name')
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = workevents
        fields = [
            'id',
            'workitems',
            'from_state',
            'to_state',
            'interim_state',
            'from_party',
            'to_party',
            'event_user',
            'display_name',
            'record_datas',
            'created_date',
            'type'
        ]

    def get_display_name(self,obj):
        return obj.event_user.display_name



# WORKFLOW-ITEMS SERIALIZER

class Workitemserializer(serializers.ModelSerializer):
    workflowevent = Workeventsserializer(many=True, read_only=True)
    current_from_party = serializers.SlugRelatedField(read_only=True, slug_field='name')
    current_to_party = serializers.SlugRelatedField(read_only=True, slug_field='name')
    wf_item_id = serializers.SerializerMethodField()
    user = serializers.SlugRelatedField(read_only=True, slug_field='email')

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
            'user',
            'created_date',
            'action',
            'subaction',
            'workflowevent'

        ]
        # read_only_fields = ['workflowevent']

    def get_wf_item_id(self,obj):
        return obj.id



# PROGRAM SERIALIZER

class ProgramListserializer(serializers.ModelSerializer):
    workflowitems = Workitemserializer(read_only=True)
    workevents = Workeventsserializer(read_only=True)
    party = serializers.SlugRelatedField(read_only=True, slug_field='name')
    created_by = serializers.SerializerMethodField()
    created_date = serializers.SerializerMethodField()
    wf_item_id = serializers.SerializerMethodField()

    class Meta:
        model = Programs
        fields = [
            "id",
            "wf_item_id",
            "party",
            'created_by',
            'created_date',
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
        return obj.workflowitems.user.email

    def get_wf_item_id(self,obj):
        return obj.workflowitems.id

    def get_created_date(self,obj):
        return obj.workflowitems.created_date



# PROGRAM CREATE SERIALIZER

class Programcreateserializer(serializers.Serializer):

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
    id = serializers.IntegerField(read_only=True)
    party = serializers.PrimaryKeyRelatedField(queryset=Parties.objects.all(),required = False)
    program_type = serializers.ChoiceField(choices=program_type)
    finance_request_type = serializers.ChoiceField(choices=finance_request_type, default=None)
    limit_currency = serializers.CharField()
    total_limit_amount = serializers.DecimalField(max_digits=8, decimal_places=2)
    # finance_currency = serializers.CharField(required=False)
    settlement_currency = serializers.CharField()
    expiry_date = serializers.DateField(format="%d-%m-%Y")
    max_finance_percentage = serializers.DecimalField(max_digits=8, decimal_places=2)
    max_invoice_age_for_funding = serializers.IntegerField()
    # max_age_for_repayment = serializers.IntegerField(required = False)
    # minimum_period = serializers.IntegerField(required = False)
    # maximum_period = serializers.IntegerField(required = False)
    maximum_amount = serializers.DecimalField(max_digits=8, decimal_places=2)
    # minimum_amount = serializers.DecimalField(max_digits=8, decimal_places=2,required=False)
    # financed_amount = serializers.DecimalField(max_digits=8, decimal_places=2,required = False)
    # balance_amount = serializers.DecimalField(max_digits=8, decimal_places=2,required = False)
    grace_period = serializers.IntegerField()
    interest_type = serializers.ChoiceField(choices=interest_type)
    interest_rate_type = serializers.ChoiceField(choices=interest_rate_type)
    # interest_rate = serializers.DecimalField(max_digits=8, decimal_places=2,required = False)
    margin = serializers.DecimalField(max_digits=8, decimal_places=2)
    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(),required = False)
    event_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),required = False)
    comments = serializers.CharField(required = False)
    # sign = serializers.PrimaryKeyRelatedField(queryset = signatures.objects.all())
    # record_datas = serializers.JSONField()
    from_party = serializers.PrimaryKeyRelatedField(queryset=Parties.objects.all(),required  = False)
    to_party = serializers.PrimaryKeyRelatedField(queryset=Parties.objects.all(),required = False)
    

    def create(self, validated_data):
        party = validated_data.pop('party')
        program_type = validated_data.pop('program_type')
        finance_request_type = validated_data.pop('finance_request_type')
        limit_currency = validated_data.pop('limit_currency')
        total_limit_amount = validated_data.pop('total_limit_amount')
        # finance_currency = validated_data.pop('finance_currency')
        settlement_currency = validated_data.pop('settlement_currency')
        expiry_date = validated_data.pop('expiry_date')
        max_finance_percentage = validated_data.pop('max_finance_percentage')
        max_invoice_age_for_funding = validated_data.pop('max_invoice_age_for_funding')
        # max_age_for_repayment = validated_data.pop('max_age_for_repayment')
        # minimum_period = validated_data.pop('minimum_period')
        # maximum_period = validated_data.pop('maximum_period')
        maximum_amount = validated_data.pop('maximum_amount')
        # minimum_amount = validated_data.pop('minimum_amount')
        # financed_amount = validated_data.pop('financed_amount')
        # balance_amount = validated_data.pop('balance_amount')
        grace_period = validated_data.pop('grace_period')
        from_party = validated_data.pop('from_party')
        to_party = validated_data.pop('to_party')
        user = validated_data.pop('user')
        interest_type = validated_data.pop('interest_type')
        interest_rate_type = validated_data.pop('interest_rate_type')
        # interest_rate = validated_data.pop('interest_rate')
        margin = validated_data.pop('margin')
        comments = validated_data.pop('comments')
        event_user = validated_data.pop('event_user')
        # sign = validated_data.pop('sign')
        # record_datas = validated_data.pop('record_datas')

        # program = Programs.objects.create(**validated_data,
        #     party=party, program_type=program_type, finance_request_type=finance_request_type,
        #     limit_currency=limit_currency, total_limit_amount=total_limit_amount, finance_currency=finance_currency,
        #     settlement_currency=settlement_currency, expiry_date=expiry_date, max_finance_percentage=max_finance_percentage,
        #     max_invoice_age_for_funding=max_invoice_age_for_funding, max_age_for_repayment=max_age_for_repayment,
        #     minimum_amount=minimum_amount, minimum_period=minimum_period, maximum_amount=maximum_amount,
        #     maximum_period=maximum_period, financed_amount=financed_amount, balance_amount=balance_amount,
        #     grace_period=grace_period, interest_rate=interest_rate, interest_rate_type=interest_rate_type,
        #     interest_type=interest_type, margin=margin , comments = comments
        # )
        program = Programs.objects.create(**validated_data,
            party=party, program_type=program_type, finance_request_type=finance_request_type,
            limit_currency=limit_currency, total_limit_amount=total_limit_amount, 
            settlement_currency=settlement_currency, expiry_date=expiry_date, max_finance_percentage=max_finance_percentage,
            max_invoice_age_for_funding=max_invoice_age_for_funding,  maximum_amount=maximum_amount,
            grace_period=grace_period, interest_rate_type=interest_rate_type,
            interest_type=interest_type, margin=margin , comments = comments
        )
        
        program.save()
        work = workflowitems.objects.create(
            program=program, current_from_party=from_party,current_to_party=to_party, user = user)
        work.save()
        
        type = {
            "comments" : []
        }
        event = workevents.objects.create( event_user = event_user , record_datas = type,workitems=work, from_party=from_party, to_party=to_party , type = "PROGRAM")
        event.save()
        return program

    


class programupdateserilizer(serializers.Serializer):

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

    party = serializers.PrimaryKeyRelatedField(queryset=Parties.objects.all(),required = False)
    program_type = serializers.ChoiceField(choices=program_type,required = False)
    finance_request_type = serializers.ChoiceField(choices=finance_request_type, default=None,required = False)
    limit_currency = serializers.CharField(required = False)
    total_limit_amount = serializers.DecimalField(max_digits=8, decimal_places=2,required = False)
    finance_currency = serializers.CharField(required = False)
    settlement_currency = serializers.CharField(required = False)
    expiry_date = serializers.DateField(format="%d-%m-%Y",required = False)
    max_finance_percentage = serializers.DecimalField(max_digits=8, decimal_places=2,required = False)
    max_invoice_age_for_funding = serializers.IntegerField(required = False)
    max_age_for_repayment = serializers.IntegerField(required = False)
    minimum_period = serializers.IntegerField(required = False)
    maximum_period = serializers.IntegerField(required = False)
    maximum_amount = serializers.DecimalField(max_digits=8, decimal_places=2,required = False)
    minimum_amount = serializers.DecimalField(max_digits=8, decimal_places=2,required = False)
    financed_amount = serializers.DecimalField(max_digits=8, decimal_places=2,required = False)
    balance_amount = serializers.DecimalField(max_digits=8, decimal_places=2,required = False)
    grace_period = serializers.IntegerField(required = False)
    interest_type = serializers.ChoiceField(choices=interest_type,required = False)
    interest_rate_type = serializers.ChoiceField(choices=interest_rate_type,required = False)
    interest_rate = serializers.DecimalField(max_digits=8, decimal_places=2,required = False)
    margin = serializers.DecimalField(max_digits=8, decimal_places=2,required = False)
    comments = serializers.CharField()

    def update(self, instance, validated_data):
        instance.party = validated_data.get('party',instance.party)
        instance.program_type = validated_data.get('program_type',instance.program_type)
        instance.finance_request_type = validated_data.get('finance_request_type',instance.finance_request_type)
        instance.limit_currency = validated_data.get('limit_currency',instance.limit_currency)
        instance.total_limit_amount = validated_data.get('total_limit_amount',instance.total_limit_amount)
        instance.finance_currency = validated_data.get('finance_currency',instance.finance_currency)
        instance.settlement_currency = validated_data.get('settlement_currency',instance.settlement_currency)
        instance.max_finance_percentage = validated_data.get('max_finance_percentage',instance.max_finance_percentage)
        instance.max_invoice_age_for_funding = validated_data.get('max_invoice_age_for_funding',instance.max_invoice_age_for_funding)
        instance.max_age_for_repayment = validated_data.get('max_age_for_repayment',instance.max_age_for_repayment)
        instance.minimum_period = validated_data.get('minimum_period',instance.minimum_period)
        instance.maximum_period = validated_data.get('maximum_period',instance.maximum_period)
        instance.maximum_amount = validated_data.get('maximum_amount',instance.maximum_amount)
        instance.minimum_amount = validated_data.get('minimum_amount',instance.minimum_amount)
        instance.financed_amount = validated_data.get('financed_amount',instance.financed_amount)
        instance.balance_amount = validated_data.get('balance_amount',instance.balance_amount)
        instance.grace_period = validated_data.get('grace_period',instance.grace_period)
        instance.interest_type = validated_data.get('interest_type',instance.interest_type)
        instance.interest_rate_type = validated_data.get('interest_rate_type',instance.interest_rate_type)
        instance.interest_rate = validated_data.get('interest_rate',instance.interest_rate)
        instance.margin = validated_data.get('margin',instance.margin)
        instance.comments = validated_data.get('comments',instance.comments)
        instance.save()
        return instance


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
            invoice=invoice, current_from_party=from_party,current_to_party=to_party, user=event_user)
        work.save()
        event = workevents.objects.create(
            workitems=work, from_party=from_party, to_party=to_party,event_user = event_user ,type = "INVOICE")
        event.save()
        return invoice


class WorkeventInvoicesserializer(serializers.ModelSerializer):
    from_party = serializers.SlugRelatedField(read_only=True, slug_field='name')
    to_party = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = workevents
        fields = [
            'id',
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
            'user',
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
    wf_item_id = serializers.SerializerMethodField()
    finance_currency_type = serializers.SlugRelatedField(read_only=True, slug_field='description')
    settlement_currency_type = serializers.SlugRelatedField(read_only=True, slug_field='description')
    invoice_currency = serializers.SlugRelatedField(read_only=True, slug_field='description')

    class Meta:
        model = Invoices
        fields = [
            'id',
            'wf_item_id',
            'party',
            'program_type',
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
        return obj.workflowitems.user.email

    def get_wf_item_id(self,obj):
        return obj.workflowitems.id


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

    id = serializers.IntegerField(read_only=True)
    wf_item_id = serializers.SerializerMethodField()
    program_type = serializers.ChoiceField(choices = program_type)
    invoices = serializers.JSONField()
    event_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),required=False)
    to_party = serializers.PrimaryKeyRelatedField(queryset = Parties.objects.all(),required = False)
    from_party = serializers.PrimaryKeyRelatedField(queryset = Parties.objects.all(),required = False)


    def create(self, validated_data):
        program_type = validated_data.pop('program_type')
        invoices = validated_data.pop('invoices')
        event_user = validated_data.pop('event_user')
        from_party = validated_data.pop('from_party')
        to_party = validated_data.pop('to_party')
        
        uploads = Invoiceuploads.objects.create(program_type = program_type , invoices = invoices ,**validated_data)
        work = workflowitems.objects.create(
            uploads=uploads, current_from_party=from_party,current_to_party=to_party, user=event_user)
        event = workevents.objects.create( event_user = event_user , type = "UPLOAD",
            workitems=work, from_party=from_party, to_party=to_party) 
        uploads.save()
        work.save()
        event.save()
        return uploads

    def get_wf_item_id(self,obj):
        return obj.workflowitems.id



class WorkeventInvoiceUploadsserializer(serializers.ModelSerializer):
    from_party = serializers.SlugRelatedField(read_only=True, slug_field='name')
    to_party = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = workevents
        fields = [
            'id',
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
            'user',
            'created_date',
            'action',
            'subaction',
            'workflowevent'

        ]
        read_only_fields = ['workflowevent']
    
    def get_wf_item_id(self,obj):
        return obj.id


# INVOICE UPLOAD SERIALIZER 

class InvoiceUploadlistserializer(serializers.ModelSerializer):
    workflowitems = WorkitemInvoiceUploadserializer(read_only=True)
    workevents = WorkeventInvoiceUploadsserializer(read_only=True)
    created_by = serializers.SerializerMethodField()
    wf_item_id = serializers.SerializerMethodField()
    final = serializers.SerializerMethodField()

    class Meta:
        model = Invoiceuploads
        fields = [
            'id',
            'wf_item_id',
            'program_type',
            'final',
            'created_by',
            'invoices',
            'workflowitems',
            'workevents'
        ]
    

    def get_created_by(self,obj):
        return obj.workflowitems.user.email

    def get_wf_item_id(self,obj):
        return obj.workflowitems.id

    def get_final(self,obj):
        queryset = workevents.objects.filter(workitems = obj.workflowitems.id).last()
        return queryset.c_final


#--------------------------------------

# END OF INVOICE UPLOAD

#-------------------------------------


# COUNTERPARTY CREATE SERIALIZER

class CounterPartySerializer(serializers.Serializer):
    interest_type = [
        ('FIXED', 'FIXED'),
        ('FLOATING', 'FLOATING')
    ]

    interest_rate_type = [
        ('LIBOR', 'LIBOR'),
        ('EURIBOR', 'EURIBOR'),
        ('SOFOR', 'SOFOR')
    ]
    
    customer_id = serializers.CharField()
    name = serializers.CharField()
    address_line_1 = serializers.CharField()
    address_line_2 = serializers.CharField()
    base_currency = serializers.PrimaryKeyRelatedField(queryset= Currencies.objects.all())
    city = serializers.CharField()
    state = serializers.CharField()
    zipcode = serializers.CharField()
    country_code = serializers.PrimaryKeyRelatedField(queryset = Countries.objects.all())
    counterparty_email = serializers.EmailField()
    counterparty_mobile = serializers.CharField()
    finance_request_type = serializers.CharField()
    limit_amount_type = serializers.PrimaryKeyRelatedField(queryset = Currencies.objects.all())
    limit_amount = serializers.IntegerField()
    expiry_date = serializers.DateField(format="%d-%m-%Y")
    max_invoice_type = serializers.PrimaryKeyRelatedField(queryset = Currencies.objects.all(),required=False)
    max_invoice_amount = serializers.IntegerField()
    max_invoice_percent = serializers.IntegerField(required=False)
    max_tenor = serializers.IntegerField()
    grace_period = serializers.IntegerField()
    interest_type = serializers.ChoiceField(choices = interest_type )
    interest_rate_type = serializers.ChoiceField(choices = interest_rate_type)
    margin = serializers.IntegerField()
    program_id = serializers.PrimaryKeyRelatedField(queryset = Programs.objects.all())
    program_type = serializers.CharField(required = False)
    
    def create(self, validated_data):
        customer_id = validated_data.pop('customer_id')
        name = validated_data.pop('name')
        finance_request_type = validated_data.pop('finance_request_type')
        address_line_1 = validated_data.pop('address_line_1')
        address_line_2 = validated_data.pop('address_line_2')
        base_currency = validated_data.pop('base_currency')
        city = validated_data.pop('city')
        state = validated_data.pop('state')
        zipcode = validated_data.pop('zipcode')
        country_code  = validated_data.pop('country_code')
        counterparty_email = validated_data.pop('counterparty_email')
        counterparty_mobile = validated_data.pop('counterparty_mobile')
        # invoice_amount = validated_data.pop('invoice_amount')
        limit_amount_type = validated_data.pop('limit_amount_type')
        limit_amount = validated_data.pop('limit_amount')
        expiry_date = validated_data.pop('expiry_date')
        max_invoice_type = validated_data.pop('max_invoice_type')
        max_invoice_amount = validated_data.pop('max_invoice_amount')
        max_invoice_percent = validated_data.pop('max_invoice_percent')
        max_tenor = validated_data.pop('max_tenor')
        grace_period = validated_data.pop('grace_period')
        interest_type = validated_data.pop('interest_type')
        interest_rate_type = validated_data.pop('interest_rate_type')
        program_id = validated_data.pop('program_id')
        margin = validated_data.pop('margin')
        pg_type = validated_data.pop('program_type')

        if pg_type == "APF":
            party = Parties.objects.create(customer_id = customer_id , name = name , base_currency = base_currency ,
            address_line_1 = address_line_1 , address_line_2 = address_line_2, city = city , state = state , zipcode = zipcode, country_code = country_code , party_type = "SELLER" ,**validated_data)
            party.save()
        else:
            party = Parties.objects.create(customer_id = customer_id , name = name , base_currency = base_currency ,
            address_line_1 = address_line_1 , address_line_2 = address_line_2, city = city , state = state , zipcode = zipcode, country_code = country_code , party_type = "BUYER" ,**validated_data)
            party.save()

        # creating  a user 
        users = User.objects.create(phone = counterparty_mobile , email = counterparty_email , party = party , first_name = "null" , last_name = "null" , display_name = "null") 
        users.save()

        # creating a pairing 
        pairs = Pairings.objects.create(program_id = program_id ,finance_request = finance_request_type, counterparty_id = party , total_limit = limit_amount , grace_period = grace_period ,
        maximum_amount = max_invoice_amount , interest_type = interest_type , interest_rate_type=interest_rate_type  , 
        minimum_amount_currency = str(limit_amount_type) , expiry_date = expiry_date , financed_amount = max_tenor , margin = margin  )
        
        pairs.save()
        return pairs


    def validate_customer_id(self,value):
        if Parties.objects.filter(customer_id = value).exists():
            raise serializers.ValidationError("A party with this customer_id / account already exists , try with other customer_id")
        return value

    def validate_name(self,value):
        if Parties.objects.filter(name = value).exists():
            raise serializers.ValidationError("A party with this name already exists , try with other name")
        return value

    def validate_counterparty_email(self,value):
        if User.objects.filter(email = value).exists():
            raise serializers.ValidationError("A User with this email already exists ")
        return value

    def validate_counterparty_mobile(self,value):
        if User.objects.filter(phone = value).exists():
            raise serializers.ValidationError("A User with this phone number already exists ")
        return value


# COUNTER PARTY LIST SERIALIZERS

class CounterPartyListSerializer(serializers.ModelSerializer):
    country_code = serializers.SlugRelatedField(read_only=True, slug_field='country')
    base_currency = serializers.SlugRelatedField(read_only=True, slug_field='description')
    limit = serializers.SerializerMethodField()
    max_Invoice_Amount = serializers.SerializerMethodField()
    grace_period = serializers.SerializerMethodField()
    Interest_Rate_Type = serializers.SerializerMethodField()
    Margin = serializers.SerializerMethodField()
    expiry_Date = serializers.SerializerMethodField()
    max_invoice_pct = serializers.SerializerMethodField()
    max_tenor = serializers.SerializerMethodField()
    interest_type = serializers.SerializerMethodField()
    program_type = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()

    class Meta:
        model = Parties
        fields = [
            'id',
            'name',
            'email',
            'phone',
            'customer_id',
            'address_line_1',
            'address_line_2',
            'onboarded',
            'party_type',
            'city',
            'base_currency',
            'state',
            'zipcode',
            'country_code',
            'party_type',
            'pairings',
            'limit',
            'max_Invoice_Amount',
            'grace_period',
            'Interest_Rate_Type',
            'Margin',
            'expiry_Date',
            'max_invoice_pct',
            'max_tenor',
            'interest_type',
            'program_type'
        ]

    def get_email(self,obj):
        cs = User.objects.get(party__name__contains = obj.name)
        return cs.email
       
    def get_phone(self,obj):
        cs = User.objects.get(party__name__contains = obj.name)
        return cs.phone
        
    def get_limit(self,obj):
        return obj.pairings.total_limit

    def get_max_Invoice_Amount(self,obj):
        return obj.pairings.maximum_amount

    def get_grace_period(self,obj):
        return obj.pairings.grace_period

    def get_Interest_Rate_Type(self,obj):
        return obj.pairings.interest_rate_type

    def get_Margin(self,obj):
        return obj.pairings.margin
    
    def get_program_type(self,obj):
        return obj.pairings.program_id.program_type

    def get_expiry_Date(self, obj):
        return obj.pairings.expiry_date

    def get_max_invoice_pct(self,obj):
        return obj.pairings.max_finance_percentage
    
    def get_max_tenor(self,obj):
        return obj.pairings.financed_amount

    def get_interest_type(self,obj):
        return obj.pairings.interest_type
