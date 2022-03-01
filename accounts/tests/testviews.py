from django.test import TestCase , Client
from django.contrib.auth import login , logout , authenticate
from accounts.models import PhoneOTP, User , Parties , Currencies , Countries 
from django.contrib.sessions.models import Session
import datetime
from django.core import mail
from django.conf import settings

email = 'test@tester.com'
phone = '1234567890'

class mytest2(TestCase):

    def test(self): 
        currency = Currencies.objects.create(iso='123', description='INR')
        country = Countries.objects.create(country="INDIA")
        party = Parties.objects.create(customer_id='123456', name='FORD', base_currency=currency, address_line_1='TEST', address_line_2='TEST',
                                       city='CHENNAI', state='TAMILNADU', zipcode='500500', country_code=country, onboarded=False, party_type='CUSTOMER')
        user = User.objects.create(email=email, phone=phone, first_name='test', last_name='tester', party = party,
                                   display_name='tester from xyz',  created_date=datetime.datetime.now(), is_administrator=False)
        user.save()
        c = Client()
        csrf_client = Client(enforce_csrf_checks=True)
        res = c.post('/api-auth/login/',{
            'email' : email,
            'phone' : phone
        })
        print(res.status_code)
        print("-------------- \n CASE 4 : USER LOGIN JSON RESPONSE \n\n",res.getvalue())
        ress = c.get('/api-auth/user/')
        print("-------------- \n CASE 5 : USER LIST API RESPONSE (TEST)\n\n",ress.getvalue())
        user_id = c.get('/api-auth/user/2/',)
        print("-------------- \n CASE 6 : USER GET BASED ON PK \n\n",user_id.getvalue())
        logs = c.post('api-auth/logout/')
        


    def test2(self):
        currency = Currencies.objects.create(iso='123', description='INR')
        country = Countries.objects.create(country="INDIA")
        party = Parties.objects.create(customer_id='123456', name='FORD', base_currency=currency, address_line_1='TEST', address_line_2='TEST',
                                       city='CHENNAI', state='TAMILNADU', zipcode='500500', country_code=country, onboarded=False, party_type='CUSTOMER')
        user = User.objects.create(email=email, phone=phone, first_name='test', last_name='tester', party = party,
                                   display_name='tester from xyz',  created_date=datetime.datetime.now(), is_administrator=False)
        user.save()
        c = Client()
        res = c.login(email =email,phone = phone)
        req = authenticate(email = email , phone = phone)
        print("-------------- \n CASE 7 : CUSTOM_MODEL_BACKEND_AUTH_LOGIN \n ",res)
    

    def test_email(self):
        email_from = settings.EMAIL_HOST_USER
        email = mail.EmailMessage(
            'TEST FROM FIN-FLO', 'THIS IS A TEST MESSAGE FROM FIN-FLO',
            email_from, ['anand98.ar@gmail.com'],
        )
        email.send(fail_silently=False)
        self.assertEqual(len(mail.outbox), 1)
    

    def test_otp_v(self):
        currency = Currencies.objects.create(iso='123', description='INR')
        country = Countries.objects.create(country="INDIA")
        party = Parties.objects.create(customer_id='123456', name='FORD', base_currency=currency, address_line_1='TEST', address_line_2='TEST',
                                       city='CHENNAI', state='TAMILNADU', zipcode='500500', country_code=country, onboarded=False, party_type='CUSTOMER')
        user = User.objects.create(email=email, phone=phone, first_name='test', last_name='tester', party = party,
                                   display_name='tester from xyz',  created_date=datetime.datetime.now(), is_administrator=False)
        user.save()
        c = Client()
        ress = c.post('/api-auth/otp/',{
            'email' : email,
            'phone' : phone
        })
        type = PhoneOTP.objects.filter(email = email )
        use = type.last()
        req = c.post('/api-auth/otp-v/?email=test@tester.com&phone=1234567890',{
            'otp' : use.otp
        })
        print("-------------- \n CASE 8 : OTP_SENT AND VERIFY LOGIN SUCCESS \n ",req.getvalue())

    
