from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.enums import Choices
from transaction.models import Actions, Programs, submodels


# BASE USER
class User(AbstractUser):

    ROLES = [
        (1, 'Bank'),
        (2, 'Parties'),
        (3, 'Customers')
    ]
    phone = models.CharField(max_length=13)
    user_type = models.CharField(
        null=True, blank=True, choices=ROLES, max_length=10)


# OTHER FIELDS ///

class Currencies(models.Model):
    iso = models.IntegerField()
    description = models.CharField(max_length=10)

    def __str__(self):
        return self.description


class Countries(models.Model):
    country = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.country


# BANK USER MODEL

class Banks(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, null=True, blank=True)
    address_line_1 = models.CharField(max_length=30)
    address_line_2 = models.CharField(max_length=20)
    city = models.CharField(max_length=35)
    state = models.CharField(max_length=35)
    zipcode = models.CharField(max_length=6)
    country_code = models.ForeignKey(Countries, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (self.name, self.country_code)


# COMPANY OR PARTIES USER MODELS

class Parties(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_id = models.CharField(max_length=18)
    name = models.CharField(max_length=35)
    base_currency = models.ForeignKey(Currencies, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=35)
    address_line_2 = models.CharField(max_length=35)
    city = models.CharField(max_length=35)
    state = models.CharField(max_length=35)
    zipcode = models.CharField(max_length=6)
    country_code = models.ForeignKey(Countries, on_delete=models.DO_NOTHING)
    onboarded = models.BooleanField(default=False)
    party_type = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Partyaccounts(models.Model):
    account_number = models.CharField(max_length=34)
    currency = models.ForeignKey(Currencies, on_delete=models.DO_NOTHING)
    party_id = models.ForeignKey(Parties, on_delete=models.DO_NOTHING)
    account_with_bank = models.ForeignKey(Banks, on_delete=models.DO_NOTHING)


# CUSTOMER USER MODEL FIELDS

class customer(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=15)
    display_name = models.CharField(max_length=55)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    party = models.ForeignKey(
        Parties, on_delete=models.CASCADE, related_name='Parties')
    is_supervisor = models.BooleanField(default=False)
    is_administrator = models.BooleanField(default=False)

    def __str__(self):
        return "%s - %s" % (self.display_name, self.user)


class user_process_auth(models.Model):
    user_id = models.ForeignKey(customer, on_delete=models.CASCADE)
    model_id = models.ForeignKey(submodels, on_delete=models.CASCADE)
    action = models.ForeignKey(Actions, on_delete=models.CASCADE)
    data_entry = models.BooleanField(default=False)
    sign_A = models.BooleanField(default=False)
    sign_B = models.BooleanField(default=False)
    sign_C = models.BooleanField(default=False)


class workflowitems(models.Model):
    STATE_TYPE = [
        ('DRAFT', 'DRAFT'),
        ('SIGN_A', 'SIGN_A'),
        ('SIGN_B', 'SIGN_B'),
        ('SIGN_C', 'SIGN_C'),
        ('AW_AP', 'AW_AP')
    ]
    created_date = models.DateTimeField(auto_now_add=True)
    program = models.OneToOneField(Programs, on_delete=models.CASCADE)
    initial_state = models.CharField(
        choices=STATE_TYPE, default='DRAFT', max_length=15)
    current_state = models.CharField(
        choices=STATE_TYPE, default='DRAFT', max_length=15)


class workevents(models.Model):
    STATE_TYPE = [
        ('DRAFT', 'DRAFT'),
        ('SIGN_A', 'SIGN_A'),
        ('SIGN_B', 'SIGN_B'),
        ('SIGN_C', 'SIGN_C'),
        ('AW_AP', 'AW_AP')
    ]
    workitems = models.ForeignKey(
        workflowitems, on_delete=models.CASCADE, related_name='workflowevent')
    event_user = models.ForeignKey(
        customer, on_delete=models.CASCADE, related_name='customername')
    record_datas = models.JSONField()
    # from_state = FSMField(choices = STATE_TYPE , default = )
