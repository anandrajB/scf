from django.test import TestCase, Client
from django.contrib.auth import login, logout, authenticate
from accounts.models import PhoneOTP, User, Parties, Currencies, Countries
from transaction.models import Programs
from django.contrib.sessions.models import Session
import datetime

email = 'test@tester.com'
phone = '1234567890'


class myTest3(TestCase):

    def test(self):
        currency = Currencies.objects.create(iso='123', description='INR')
        country = Countries.objects.create(country="INDIA")
        party = Parties.objects.create(customer_id='098765', name='RENAULT', base_currency=currency, address_line_1='TEST', address_line_2='TEST',
                                       city='CHENNAI', state='TAMILNADU', zipcode='500500', country_code=country, onboarded=False, party_type='BUYER')
        user = User.objects.create(email=email, phone=phone, first_name='test', last_name='tester', party=party,
                                   display_name='tester from xyz',  created_date=datetime.datetime.now(), is_administrator=False)
        user.save()

        c = Client()
        csrf_client = Client(enforce_csrf_checks=True)
        res = c.post('/api-auth/login/', {
            'email': email,
            'phone': phone
        })

        res_pro = c.post('/api/program/', {
            'party': 1,
            'program_type': 'APF',
            'finance_request_type': 'ON_REQUEST',
            'limit_currency': 12,
            'total_limit_amount': 10,
            'finance_currency': 12,
            'settlement_currency': 12,
            'expiry_date': '2022-02-11',
            'max_finance_percentage': 75,
            'max_invoice_age_for_funding': 100,
            'max_age_for_repayment': 2,
            'minimum_period': 1,
            'maximum_period': 2,
            'maximum_amount': 110,
            'minimum_amount': 120,
            'financed_amount': 90,
            'balance_amount': 50,
            'grace_period': 5,
            'interest_type': 'FIXED',
            'interest_rate_type': 'LIBOR',
            'interest_rate': 15,
            'margin': 10,
            'comments': "comments"
        })
    
        print(f"Status of login   => {res.status_code}")
        print(f"Status of program => {res_pro.status_code}")
        print("-------------- \n CASE 4 : USER LOGIN JSON RESPONSE \n\n", res.getvalue())
        ress = c.get('/api-auth/user/')
        print(
            "-------------- \n CASE 5 : USER LIST API RESPONSE (TEST)\n\n", ress.getvalue())
        user_id = c.get('/api-auth/user/1/',)
        print("-------------- \n CASE 6 : USER GET BASED ON PK \n\n",
              user_id.getvalue())
        logs = c.post('api-auth/logout/')
        print("Program response", res_pro.getvalue())

    def test2(self):
        currency = Currencies.objects.create(iso='123', description='INR')
        country = Countries.objects.create(country="INDIA")
        party = Parties.objects.create(customer_id='098765', name='TATA', base_currency=currency, address_line_1='TEST', address_line_2='TEST',
                                       city='CHENNAI', state='TAMILNADU', zipcode='500500', country_code=country, onboarded=False, party_type='BUYER')
        user = User.objects.create(email=email, phone=phone, first_name='test', last_name='tester', party=party,
                                   display_name='tester from xyz',  created_date=datetime.datetime.now(), is_administrator=False)
        user.save()

        c = Client()
        csrf_client = Client(enforce_csrf_checks=True)
        res = c.post('/api-auth/login/', {
            'email': email,
            'phone': phone
        })

        res_pro = c.post('/api/program/', {
            'party': 1,
            'program_type': 'APF',
            'finance_request_type': 'ON_REQUEST',
            'limit_currency': 12,
            'total_limit_amount': 10,
            'finance_currency': 12,
            'settlement_currency': 12,
            'expiry_date': '2022-02-11',
            'max_finance_percentage': 75,
            'max_invoice_age_for_funding': 100,
            'max_age_for_repayment': 2,
            'minimum_period': 1,
            'maximum_period': 2,
            'maximum_amount': 110,
            'minimum_amount': 120,
            'financed_amount': 90,
            'balance_amount': 50,
            'grace_period': 5,
            'interest_type': 'FIXED',
            'interest_rate_type': 'LIBOR',
            'interest_rate': 15,
            'margin': 10,
            'comments': "comments"
        })

        res_pair = c.post('/api/pairing/', {
            'program_id': 1,
            'counterparty_id': 1,
            'finance_request': 'AUTOMATIC',
            'currency': 1,
            'total_limit': 12,
            'finance_currency_type': 1,
            'settlement_currency_type': 1,
            'expiry_date': '2022-03-29',
            'max_finance_percentage': 35,
            'max_invoice_age_for_funding': 20,
            'max_age_for_repayment': 10,
            'minimum_period': 1,
            'maximum_period': 10,
            'minimum_amount_currency': 10,
            'minimum_amount': 100,
            'maximum_amount': 200,
            'financed_amount': 100,
            'balance_amount': 50,
            'grace_period': 5,
            'interest_type': 'FIXED',
            'interest_rate_type': 'LIBOR',
            'interest_rate': 10,
            'margin': 10,
            'created_date': "2022-01-19"
        })

        print(f"Status of login   => {res.status_code}")
        print(f"Status of program => {res_pro.status_code}")
        print(f"Status of pairing => {res_pair.status_code}")
        print(f"Response => {res_pair.getvalue()}")
