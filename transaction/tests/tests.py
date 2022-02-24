from django.test import TestCase, Client
from rest_framework.test import APITestCase
from transaction.models import Pairings, submodels, Programs, workflowitems, workevents, Invoices, Invoiceuploads
from accounts.models import Currencies, Countries, Parties, User, userprocessauth, Action
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
        user = User.objects.create(email=email, phone=phone, first_name='test', last_name='tester', party=party,
                                   display_name='tester from xyz', created_date=datetime.datetime.now(), is_administrator=False)
        action = Action.objects.create(desc='SUBMIT')
        userprocess = userprocessauth.objects.create(
            user=user, action=action, model="PROGRAM", data_entry=True, sign_a=True, sign_b=False, sign_c=False)
        user.save()
        ss = submodels.objects.create(
            description="test", api_route='test_user')
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
            program=program, current_from_party=party, current_to_party=party2, event_users=user)
        work.save()
        event = workevents.objects.create(
            workitems=work, from_party=party2, to_party=party2)
        event.save()
        print("1")
        program2 = Programs.objects.create(
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
            program=program2, current_from_party=party, current_to_party=party2, event_users=user)
        work.save()
        event = workevents.objects.create(
            workitems=work, from_party=party2, to_party=party2)
        event.save()
        print('2')
        program3 = Programs.objects.create(
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
            program=program3, current_from_party=party, current_to_party=party2, event_users=user)
        work.save()
        event = workevents.objects.create(
            workitems=work, from_party=party2, to_party=party2)
        event.save()
        program5 = Programs.objects.create(
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
            program=program5, current_from_party=party, current_to_party=party2, event_users=user)
        work.save()
        event = workevents.objects.create(
            workitems=work, from_party=party2, to_party=party2)
        event.save()
        print("-------------- \n CASE 1 : PROGRAM , WORKFLOWITEMS , WORKEVENTS CREATED \n ")

        pairing1 = Pairings.objects.create(
            program_type=program, counterparty_id=party, finance_request='AUTOMATIC', currency=currency, total_limit=100000, finance_currency_type=currency, settlement_currency_type=currency, max_finance_percentage=60, max_invoice_age_for_funding=100, max_age_for_repayment=500, minimum_period=10, maximum_period=20, minimum_amount_currency="TE1", minimum_amount=100, maximum_amount=200,
            financed_amount=1000, balance_amount=500, grace_period=2, interest_type='FIXED', interest_rate_type="LIBOR", interest_rate=10, margin=20
        )

        pairing2 = Pairings.objects.create(
            program_type=program, counterparty_id=party, finance_request='ON_REQUEST', currency=currency, total_limit=100000, finance_currency_type=currency, settlement_currency_type=currency, max_finance_percentage=60, max_invoice_age_for_funding=300, max_age_for_repayment=200, minimum_period=10, maximum_period=10, minimum_amount_currency="TE2", minimum_amount=100, maximum_amount=250,
            financed_amount=1000, balance_amount=590, grace_period=5, interest_type='FLOATING', interest_rate_type="EURIBOR", interest_rate=10, margin=20
        )

        pairing3 = Pairings.objects.create(
            program_type=program, counterparty_id=party, finance_request='AUTOMATIC', currency=currency, total_limit=10000, finance_currency_type=currency, settlement_currency_type=currency, max_finance_percentage=60, max_invoice_age_for_funding=800, max_age_for_repayment=400, minimum_period=10, maximum_period=20, minimum_amount_currency="TE3", minimum_amount=150, maximum_amount=200,
            financed_amount=2000, balance_amount=100, grace_period=10, interest_type='FIXED', interest_rate_type="LIBOR", interest_rate=10, margin=20
        )

        invoice_1 = Invoices.objects.create(pairing=pairing1,
                                            party=party, invoice_no=1, invoice_currency=currency, amount=12000,
                                            funding_req_type="AUTOMATIC", finance_currency_type=currency, settlement_currency_type=currency, interest_rate=10, financed_amount=1000, bank_loan_id=2)
        work = workflowitems.objects.create(
            invoice=invoice_1, current_from_party=party, current_to_party=party2, event_users=user
        )
        event = workevents.objects.create(
            workflowitems=work, from_party=party, to_party=party2)
        event.save()

        invoice_2 = Invoices.objects.create(pairing=pairing2,
                                            party=party, invoice_no=2, invoice_currency=currency, amount=11000,
                                            funding_req_type="AUTOMATIC", finance_currency_type=currency, settlement_currency_type=currency, interest_rate=11, financed_amount=1000, bank_loan_id=3)
        work = workflowitems.objects.create(
            invoice=invoice_2, current_from_party=party, current_to_party=party2, event_users=user
        )
        event = workevents.objects.create(
            workflowitems=work, from_party=party, to_party=party2)
        event.save()

        invoice_3 = Invoices.objects.create(pairing=pairing3,
                                            party=party, invoice_no=3, invoice_currency=currency, amount=10000,
                                            funding_req_type="AUTOMATIC", finance_currency_type=currency, settlement_currency_type=currency, interest_rate=12, financed_amount=1000, bank_loan_id=1)
        work = workflowitems.objects.create(
            invoice=invoice_3, current_from_party=party, current_to_party=party2, event_users=user
        )
        event = workevents.objects.create(
            workflowitems=work, from_party=party, to_party=party2)
        event.save()

        upload_1 = Invoiceuploads.objects.create(
            program_type="APF", invoices={'name': 'test1'}
        )
        work = workflowitems.objects.create(
            upload=upload_1, current_from_party=party, current_to_party=party2, event_users=user)
        event = workevents.objects.create(
            workflowitems=work, from_party=party, to_party=party2)
        event.save()

        upload_2 = Invoiceuploads.objects.create(
            program_type="RF", invoices={'name': 'test2'}
        )
        work = workflowitems.objects.create(
            upload=upload_2, current_from_party=party, current_to_party=party2, event_users=user)
        event = workevents.objects.create(
            workflowitems=work, from_party=party, to_party=party2)
        event.save()

        upload_3 = Invoiceuploads.objects.create(
            program_type="DF", invoices={'name': 'test3'}
        )
        work = workflowitems.objects.create(
            upload=upload_3, current_from_party=party, current_to_party=party2, event_users=user)
        event = workevents.objects.create(
            workflowitems=work, from_party=party, to_party=party2)
        event.save()
