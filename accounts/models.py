from django.db import models
from django.contrib.auth.models import BaseUserManager , AbstractBaseUser ,PermissionsMixin
from transaction.models import workevents , Programs , submodels , Actions , invoice_uploads, workflowitems


# CUSTOM USER MODEL ( PHONE / EMAIL )

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



class User(AbstractBaseUser,PermissionsMixin):
    phone = models.CharField(max_length=16, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
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

    @property
    def is_staff(self):
        return self.is_supervisor

    @property
    def is_superuser(self):
        return self.is_administrator


# OTHER FIELDS      

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

    user = models.OneToOneField(User,on_delete=models.CASCADE)
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
        return "%s - %s - %s"%(self.name,self.customer_id,self.party_type)



class Partyaccounts(models.Model):
    account_number = models.CharField(max_length=34)
    currency = models.ForeignKey(Currencies,on_delete=models.DO_NOTHING)
    party_id = models.ForeignKey(Parties,on_delete=models.DO_NOTHING)
    account_with_bank = models.ForeignKey(Banks,on_delete=models.DO_NOTHING)

    def __str__(self):
        return "%s related with party  %s"%(self.account_number , self.party_id)



# CUSTOMER USER MODEL FIELDS

class customer(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=15)
    display_name = models.CharField(max_length=55)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    party = models.ForeignKey(Parties,on_delete=models.CASCADE,related_name='Parties')
    is_supervisor = models.BooleanField(default=False)
    is_administrator = models.BooleanField(default=False)


    def __str__(self):
        return "%s - %s"%(self.display_name , self.user )

# USER PROCESS AUTH

class userprocessauth(models.Model):
    user_id = models.ForeignKey(customer,on_delete=models.CASCADE)
    model_id = models.ForeignKey(submodels,on_delete=models.CASCADE)
    action = models.ForeignKey(Actions,on_delete=models.CASCADE)
    data_entry = models.BooleanField(default=False)
    sign_A = models.BooleanField(default=False)
    sign_B = models.BooleanField(default=False)
    sign_C = models.BooleanField(default=False)

# SIGNATURE LEVELS

class signatures(models.Model):
    party_belongs = models.ForeignKey(Parties,on_delete=models.CASCADE)
    sign_a = models.BooleanField(default=False)
    sign_b = models.BooleanField(default=False)
    sign_c = models.BooleanField(default=False)
    action = models.CharField(max_length= 35,default='SUBMIT')
    workflowitem = models.ForeignKey(workflowitems,on_delete=models.CASCADE)
