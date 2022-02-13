import datetime
from django.test import SimpleTestCase , TestCase
from rest_framework.test import APITestCase
from accounts.models import Action, Banks, Currencies, Parties, Countries, Partyaccounts, User, signatures, userprocessauth
# Create your tests here.


class mytest(APITestCase):

    def test(self):
        time = datetime.datetime.now()
        currency = Currencies.objects.create(iso='123', description='INR')
        country = Countries.objects.create(country="INDIA")
        party = Parties.objects.create(customer_id='123456', name='FORD', base_currency=currency, address_line_1='TEST', address_line_2='TEST',
                                       city='CHENNAI', state='TAMILNADU', zipcode='500500', country_code=country, onboarded=False, party_type='CUSTOMER')
        bank = Banks.objects.create(name='ICICI', address_line_1='TEST', address_line_2='TEST',
                                    city='CHENNAI', state='TAMILNADU', zipcode='500500', country_code=country, created_at=time)
        Partyaccounts.objects.create(
            account_number='1234567890', currency=currency, party_id=party, account_with_bank=bank)
        print("-------------- \n CASE 1 : BANKS , PARTIES , COUNTRY , CURRENCIES CREATED")
       


    def test2(self):
        currency = Currencies.objects.create(iso='123', description='INR')
        country = Countries.objects.create(country="INDIA")
        party = Parties.objects.create(customer_id='123456', name='FORD', base_currency=currency, address_line_1='TEST', address_line_2='TEST',
                                       city='CHENNAI', state='TAMILNADU', zipcode='500500', country_code=country, onboarded=False, party_type='CUSTOMER')
        user = User.objects.create(email="test@tester.com", phone='1234567890', first_name='test', last_name='tester',
                                   display_name='tester from xyz', created_date=datetime.datetime.now(), is_administrator=False)
        action = Action.objects.create(desc = 'SUBMIT')
        userprocessauth.objects.create(
            user=user, model='PROGRAM', action=action, data_entry=False, sign_a=False, sign_b=False)
        user.delete()
        print("-------------- \n CASE 2 : USER CREATION AND USER PROCESS AUTH ")
       

    def test3(self):
        currency = Currencies.objects.create(iso='123', description='INR')
        country = Countries.objects.create(country="INDIA")
        party = Parties.objects.create(customer_id='123456', name='FORD', base_currency=currency, address_line_1='TEST', address_line_2='TEST',
                                       city='CHENNAI', state='TAMILNADU', zipcode='500500', country_code=country, onboarded=False, party_type='CUSTOMER')
        action = Action.objects.create(desc = 'SUBMIT')
        action2 = Action.objects.create(desc = 'REJECT')
        signatures.objects.create(model = 'PROGRAM' , action = action,party = party , sign_a = True )
        signatures.objects.create(model = 'PROGRAM' , action = action2,party = party , sign_b = True )
        print("-------------- \n CASE 3 : PARTY LINKED SIGNATURES CREATED")
       