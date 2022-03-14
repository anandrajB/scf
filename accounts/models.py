from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)
# from django.core.validators import RegexValidator
from rest_framework_simplejwt.tokens import RefreshToken

# OTHER MODELS


class Currencies(models.Model):
    iso = models.IntegerField()
    description = models.CharField(max_length=10)

    def save(self, *args, **kwargs):
        self.description = self.description.upper()
        return super(Currencies, self).save(*args, **kwargs)

    def __str__(self):
        return self.description


class Countries(models.Model):
    country = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.country = self.country.upper()
        return super(Countries, self).save(*args, **kwargs)

    def __str__(self):
        return self.country


# BANK USER MODEL

class Banks(models.Model):
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

    party_type_choices = [
        ('CUSTOMER', 'CUSTOMER'),
        ('BANK', 'BANK'),
        ('OTHER', 'OTHER'),
        ('SELLER', 'SELLER'),
        ('BUYER', 'BUYER'),
    ]

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
    party_type = models.CharField(choices=party_type_choices, max_length=25)

    def __str__(self):
        return self.name


class Partyaccounts(models.Model):
    account_number = models.CharField(max_length=34)
    currency = models.ForeignKey(Currencies, on_delete=models.DO_NOTHING)
    party_id = models.ForeignKey(Parties, on_delete=models.DO_NOTHING)
    account_with_bank = models.ForeignKey(Banks, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "%s related with party  %s" % (self.account_number, self.party_id)


# CUSTOM USER MODEL SETUP  ( PHONE / EMAIL )

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **kwargs):
        is_active = kwargs.pop("is_active", False)
        is_supervisor = kwargs.pop("is_supervisor", False)
        is_administrator = kwargs.pop("is_administrator", False)
        user = self.model(
            email=email,
            is_active=is_active,
            is_supervisor=is_supervisor,
            is_administrator=is_administrator,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(
            email,
            password,
            is_active=True,
            is_supervisor=True,
            is_administrator=True,
            **extra_fields
        )


# MY USER MODEL

class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=16, unique=True)
    email = models.EmailField(unique=True)
    party = models.ForeignKey(
        Parties, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True, blank=False)
    is_supervisor = models.BooleanField(default=False)
    is_administrator = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "phone"

    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    # def has_perm(self, perm, obj=None):
    #     return True

    # def has_module_perms(self, app_label):
    #     return True

    # is_supervisor -> staff user
    @property
    def is_staff(self):
        return self.is_supervisor

    # is_admin -> superuser

    @property
    def is_superuser(self):
        return self.is_administrator

    def tokens(self):
        refresh = RefreshToken.for_user(self)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


# OTP MODELS

class PhoneOTP(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=16)
    otp = models.CharField(max_length=6)

    def __str__(self):
        return "%s - %s" % (self.phone, self.otp)


# MODELS

class Models(models.Model):
    desc = models.CharField(max_length=155)
    api_route = models.CharField(max_length=155)


# ACTIONS
class Action(models.Model):
    desc = models.CharField(max_length=55)
    bank = models.BooleanField(blank=True, null=True, default=False)
    customer = models.BooleanField(default=False, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.desc = self.desc.upper()
        return super(Action, self).save(*args, **kwargs)

    def __str__(self):
        return self.desc


# SIGNATURE LEVELS

class signatures(models.Model):
    model = models.CharField(max_length=55)
    action = models.ForeignKey(Action, on_delete=models.DO_NOTHING)
    party = models.ForeignKey(Parties, on_delete=models.CASCADE)
    sign_a = models.BooleanField(default=False, blank=True, null=True)
    sign_b = models.BooleanField(default=False, blank=True, null=True)
    sign_c = models.BooleanField(default=False, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.model = self.model.upper()
        return super(signatures, self).save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['id', ]),
            models.Index(fields=['model', ]),
            models.Index(fields=['action', ]),
            models.Index(fields=['party', ]),
        ]


# USER PROCESS AUTH

class userprocessauth(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    model = models.CharField(max_length=55)
    action = models.ForeignKey(Action, on_delete=models.DO_NOTHING)
    data_entry = models.BooleanField(default=False, blank=True, null=True)
    sign_a = models.BooleanField(default=False, blank=True, null=True)
    sign_b = models.BooleanField(default=False, blank=True, null=True)
    sign_c = models.BooleanField(default=False, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.model = self.model.upper()
        return super(userprocessauth, self).save(*args, **kwargs)
