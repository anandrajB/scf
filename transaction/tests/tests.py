from django.test import TestCase , Client
from rest_framework.test import APITestCase
from transaction.models import submodels , Programs , workflowitems , workevents
from accounts.models import Currencies , Countries , Parties,User, userprocessauth
import datetime


email = 'test@tester.com'
phone = '1234567890'

# Create your tests here.
class mytestcase(TestCase):

    def test(self):
        currency = Currencies.objects.create(iso='123', description='INR')
        country = Countries.objects.create(country="INDIA")
        party = Parties.objects.create(customer_id='123456', name='FORD', base_currency=currency, address_line_1='TEST', address_line_2='TEST',
                                       city='CHENNAI', state='TAMILNADU', zipcode='500500', country_code=country, onboarded=False, party_type='CUSTOMER')
        party2 = Parties.objects.create(customer_id='12133', name='RENAULT', base_currency=currency, address_line_1='TEST', address_line_2='TEST',
                                       city='CHENNAI', state='TAMILNADU', zipcode='500500', country_code=country, onboarded=False, party_type='CUSTOMER')
        user = User.objects.create(email=email, phone=phone, first_name='test', last_name='tester', party = party,
                                   display_name='tester from xyz', created_date=datetime.datetime.now(), is_administrator=False)
        userprocess = userprocessauth.objects.create(user = user , action = "SUBMIT",model="PROGRAM",data_entry = True ,sign_a = True , sign_b = False , sign_c = False)
        user.save()
        ss=  submodels.objects.create(description = "test",api_route = 'test_user')
        ss.save()
        c = Client()
        program = Programs.objects.create(
            party=party, program_type="APF", finance_request_type="AUTOMATIC",
            limit_currency="12", total_limit_amount="12", finance_currency="12",
            settlement_currency="12", expiry_date="2022-12-12", max_finance_percentage="12",
            max_invoice_age_for_funding="12", max_age_for_repayment="12",
            minimum_amount="12", minimum_period="12", maximum_amount="12",
            maximum_period="12", financed_amount="12", balance_amount="12",
            grace_period="12", interest_rate="12", interest_rate_type="LIBOR",
            interest_type="FIXED", margin="12" 
        )
        work = workflowitems.objects.create(
            program=program, current_from_party=party,current_to_party=party2, event_users=user)
        work.save()
        event = workevents.objects.create(
            workitems=work, from_party=party2, to_party=party2)
        event.save()
        print("-------------- \n CASE 1 : PROGRAM , WORKFLOWITEMS , WORKEVENTS CREATED \n ")