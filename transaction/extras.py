




########### END ##########



# PROGRAM UPDATE API VIEW FOR PROGRAM SERIALIZER UPDATED ON  7-4-2022


# class programupdateserilizer(serializers.Serializer):

#     finance_request_type = [
#         ('AUTOMATIC', 'AUTOMATIC'),
#         ('ON_REQUEST', 'ON_REQUEST')
#     ]

#     interest_type = [
#         ('FIXED', 'FIXED'),
#         ('FLOATING', 'FLOATING')
#     ]

#     interest_rate_type = [
#         ('LIBOR', 'LIBOR'),
#         ('EURIBOR', 'EURIBOR'),
#         ('SOFOR', 'SOFOR')
#     ]

#     program_type = [
#         ('ALL', 'ALL'),
#         ('APF', 'APF'),
#         ('RF', 'RF'),
#         ('DF', 'DF')
#     ]

#     party = serializers.PrimaryKeyRelatedField(queryset=Parties.objects.all(),required = False)
#     program_type = serializers.ChoiceField(choices=program_type,required = False)
#     finance_request_type = serializers.ChoiceField(choices=finance_request_type, default=None,required = False)
#     limit_currency = serializers.CharField(required = False)
#     total_limit_amount = serializers.DecimalField(max_digits=8, decimal_places=2,required = False)
#     finance_currency = serializers.CharField(required = False)
#     settlement_currency = serializers.CharField(required = False)
#     expiry_date = serializers.DateField(format="%d-%m-%Y",required = False)
#     max_finance_percentage = serializers.DecimalField(max_digits=8, decimal_places=2,required = False)
#     max_invoice_age_for_funding = serializers.IntegerField(required = False)
#     max_age_for_repayment = serializers.IntegerField(required = False)
#     minimum_period = serializers.IntegerField(required = False)
#     maximum_period = serializers.IntegerField(required = False)
#     maximum_amount = serializers.DecimalField(max_digits=8, decimal_places=2,required = False)
#     minimum_amount = serializers.DecimalField(max_digits=8, decimal_places=2,required = False)
#     financed_amount = serializers.DecimalField(max_digits=8, decimal_places=2,required = False)
#     balance_amount = serializers.DecimalField(max_digits=8, decimal_places=2,required = False)
#     grace_period = serializers.IntegerField(required = False)
#     interest_type = serializers.ChoiceField(choices=interest_type,required = False)
#     interest_rate_type = serializers.ChoiceField(choices=interest_rate_type,required = False)
#     interest_rate = serializers.DecimalField(max_digits=8, decimal_places=2,required = False)
#     margin = serializers.DecimalField(max_digits=8, decimal_places=2,required = False)
#     comments = serializers.CharField(required = False)

#     def update(self, instance, validated_data):
#         instance.party = validated_data.get('party',instance.party)
#         instance.program_type = validated_data.get('program_type',instance.program_type)
#         instance.finance_request_type = validated_data.get('finance_request_type',instance.finance_request_type)
#         instance.limit_currency = validated_data.get('limit_currency',instance.limit_currency)
#         instance.total_limit_amount = validated_data.get('total_limit_amount',instance.total_limit_amount)
#         instance.finance_currency = validated_data.get('finance_currency',instance.finance_currency)
#         instance.settlement_currency = validated_data.get('settlement_currency',instance.settlement_currency)
#         instance.max_finance_percentage = validated_data.get('max_finance_percentage',instance.max_finance_percentage)
#         instance.max_invoice_age_for_funding = validated_data.get('max_invoice_age_for_funding',instance.max_invoice_age_for_funding)
#         instance.max_age_for_repayment = validated_data.get('max_age_for_repayment',instance.max_age_for_repayment)
#         instance.minimum_period = validated_data.get('minimum_period',instance.minimum_period)
#         instance.maximum_period = validated_data.get('maximum_period',instance.maximum_period)
#         instance.maximum_amount = validated_data.get('maximum_amount',instance.maximum_amount)
#         instance.minimum_amount = validated_data.get('minimum_amount',instance.minimum_amount)
#         instance.financed_amount = validated_data.get('financed_amount',instance.financed_amount)
#         instance.balance_amount = validated_data.get('balance_amount',instance.balance_amount)
#         instance.grace_period = validated_data.get('grace_period',instance.grace_period)
#         instance.interest_type = validated_data.get('interest_type',instance.interest_type)
#         instance.interest_rate_type = validated_data.get('interest_rate_type',instance.interest_rate_type)
#         instance.interest_rate = validated_data.get('interest_rate',instance.interest_rate)
#         instance.margin = validated_data.get('margin',instance.margin)
#         instance.comments = validated_data.get('comments',instance.comments)
#         instance.save()
#         return instance
print("hello")