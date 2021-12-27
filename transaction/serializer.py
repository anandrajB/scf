from rest_framework import serializers
from .models import Programs


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programs
        fields = [
            "id",
            "model",
            "party",
            "program_model",
            "finance_request_type",
            "currency",
            "max_total_limit",
            "expiry",
            "max_finance_percentage",
            "max_age_for_repayment",
            "minimum_period",
            'maximum_period',
            "minimum_amount_currency",
            "minimum_amount",
            "financed_amount",
            "balance_amount",
            "grace_period",
            "interest_type",
            "interest_rate",
            "margin"
        ]

        read_only_fields = [
            "id",
            "last_login",
            "date_joined",
        ]
