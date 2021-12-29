from django.utils.translation import to_language, ungettext
from rest_framework import serializers
from .models import Programs
from accounts.models import workflowitems, workevents, Parties, customer
# from accounts.serializer import Workitemserializer , Workeventsserializer


# class Workeventsserializer(serializers.ModelSerializer):
#     class Meta:
#         model = workevents
#         fields = '__all__'


# class Workitemserializer(serializers.ModelSerializer):
#     workeveenttype  = Workeventsserializer(read_only = True,many = True)
#     class Meta:
#         model = workflowitems
#         fields = [
#             'initial_state',
#             'workeveenttype'
#         ]
#         read_only_fields = ['workeveenttype']


class Workeventsserializer(serializers.ModelSerializer):
    class Meta:
        model = workevents
        fields = '__all__'


class Workitemserializer(serializers.ModelSerializer):
    workflowevent = Workeventsserializer(many=True, read_only=True)

    class Meta:
        model = workflowitems
        fields = [
            'initial_state',
            'program',
            'current_state',
            'created_date',
            'workflowevent'
        ]
        read_only_fields = ['workflowevent']


class ProgramListserializer(serializers.ModelSerializer):
    workflowitems = Workitemserializer(read_only=True)
    workevents = Workeventsserializer(read_only=True)

    class Meta:
        model = Programs
        fields = [
            "id",
            "party",
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
            'workevents'
        ]


class Programcreateserializer(serializers.Serializer):
    party = serializers.PrimaryKeyRelatedField(queryset=Parties.objects.all())
    program_type = serializers.CharField()
    finance_request_type = serializers.CharField()
    limit_currency = serializers.CharField()
    total_limit_amount = serializers.DecimalField(
        max_digits=5, decimal_places=2)
    finance_currency = serializers.CharField()
    settlement_currency = serializers.CharField()
    expiry_date = serializers.DateField()
    max_finance_percentage = serializers.DecimalField(
        max_digits=5, decimal_places=2)
    max_invoice_age_for_funding = serializers.IntegerField()
    max_age_for_repayment = serializers.IntegerField()
    minimum_period = serializers.IntegerField()
    maximum_period = serializers.IntegerField()
    maximum_amount = serializers.CharField()
    minimum_amount = serializers.DecimalField(max_digits=5, decimal_places=2)
    financed_amount = serializers.DecimalField(max_digits=5, decimal_places=2)
    balance_amount = serializers.DecimalField(max_digits=5, decimal_places=2)
    grace_period = serializers.IntegerField()
    interest_type = serializers.CharField()
    interest_rate_type = serializers.CharField()
    interest_rate = serializers.DecimalField(max_digits=6, decimal_places=2)
    margin = serializers.DecimalField(max_digits=5, decimal_places=2)
    event_user = serializers.PrimaryKeyRelatedField(
        queryset=customer.objects.all())
    record_datas = serializers.JSONField()

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
        max_invoice_age_for_funding = validated_data.pop(
            'max_invoice_age_for_funding')
        max_age_for_repayment = validated_data.pop('max_age_for_repayment')
        minimum_period = validated_data.pop('minimum_period')
        maximum_period = validated_data.pop('maximum_period')
        maximum_amount = validated_data.pop('maximum_amount')
        minimum_amount = validated_data.pop('minimum_amount')
        financed_amount = validated_data.pop('financed_amount')
        balance_amount = validated_data.pop('balance_amount')
        grace_period = validated_data.pop('grace_period')
        interest_type = validated_data.pop('interest_type')
        interest_rate_type = validated_data.pop('interest_rate_type')
        interest_rate = validated_data.pop('interest_rate')
        margin = validated_data.pop('margin')
        event_user = validated_data.pop('event_user')
        record_datas = validated_data.pop('record_datas')

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
            program=program, initial_state=finance_request_type)
        work.save()
        event = workevents.objects.create(
            workitems=work, event_user=event_user, record_datas=record_datas)
        event.save()
        return program

    def update(self, instance, validated_data):
        # check the updated here
        return super().update(instance, validated_data)
