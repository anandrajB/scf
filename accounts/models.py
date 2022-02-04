from django.db import models
from django.contrib.auth.models import BaseUserManager , AbstractBaseUser ,PermissionsMixin
from transaction.models import submodels 
from django.core.validators import MaxValueValidator , MinValueValidator
from django.core.validators import RegexValidator



# OTHER MODELS     

class Currencies(models.Model):
    iso = models.IntegerField()
    description = models.CharField(max_length=10)

    def __str__(self):
        return self.description

class Countries(models.Model):
    country = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.country



# BANK USER MODEL

class Banks(models.Model):
    name = models.CharField(max_length=40,null=True,blank=True)
    address_line_1 = models.CharField(max_length=30)
    address_line_2 = models.CharField(max_length=20)
    city = models.CharField(max_length=35)
    state = models.CharField(max_length=35)
    zipcode = models.CharField(max_length=6)
    country_code = models.ForeignKey(Countries,on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "%s - %s"%(self.name , self.country_code)


# COMPANY OR PARTIES USER MODELS 

class Parties(models.Model):

    customer_id = models.CharField(max_length=18)
    name = models.CharField(max_length=35)
    base_currency  = models.ForeignKey(Currencies,on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=35)
    address_line_2 = models.CharField(max_length=35)
    city = models.CharField(max_length=35)
    state = models.CharField(max_length=35)
    zipcode = models.CharField(max_length=6)
    country_code = models.ForeignKey(Countries,on_delete=models.DO_NOTHING)
    onboarded = models.BooleanField(default=False)
    party_type = models.CharField(max_length=15)


    def __str__(self):
        return "%s - party_type - %s"%(self.name,self.party_type)



class Partyaccounts(models.Model):
    account_number = models.CharField(max_length=34)
    currency = models.ForeignKey(Currencies,on_delete=models.DO_NOTHING)
    party_id = models.ForeignKey(Parties,on_delete=models.DO_NOTHING)
    account_with_bank = models.ForeignKey(Banks,on_delete=models.DO_NOTHING)

    def __str__(self):
        return "%s related with party  %s"%(self.account_number , self.party_id)



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

class User(AbstractBaseUser,PermissionsMixin):
    phone = models.CharField(max_length=16, unique=True)
    email = models.EmailField(unique=True)
    party = models.ForeignKey(Parties,on_delete=models.CASCADE,blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True, blank = False)
    is_supervisor = models.BooleanField(default=False)
    is_maker = models.BooleanField(default=False)
    is_sign_a = models.BooleanField(default=False)
    is_sign_b = models.BooleanField(default=False)
    is_sign_c = models.BooleanField(default=False)
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

    @property
    def is_staff(self):
        return self.is_supervisor

    @property
    def is_superuser(self):
        return self.is_administrator


# OTP MODELS 

class PhoneOTP(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=16)
    otp = models.CharField(max_length=6)

    def __str__(self):
        return "%s - %s"%(self.phone , self.otp)



# SIGNATURE LEVELS

class signatures(models.Model):
    model = models.CharField(max_length=55)
    action = models.CharField(max_length= 35,default='SUBMIT')
    party = models.ForeignKey(Parties,on_delete=models.CASCADE)
    sign_a = models.BooleanField(default=False , blank=True, null=True)
    sign_b = models.BooleanField(default=False,blank=True, null=True)
    sign_c = models.BooleanField(default=False , blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['id',]),
            models.Index(fields=['model',]),
            models.Index(fields=['action',]),
            models.Index(fields=['party',]),
        ]

    

# USER PROCESS AUTH

class userprocessauth(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    model_id = models.CharField(max_length=55)
    action = models.CharField(max_length=255)
    signature = models.ForeignKey(signatures,on_delete=models.CASCADE)
    data_entry = models.BooleanField(default=False,blank=True, null=True)
    sign_a = models.BooleanField(default=False,blank=True, null=True)
    sign_b = models.BooleanField(default=False,blank=True, null=True)
    sign_c = models.BooleanField(default=False,blank=True, null=True)
    