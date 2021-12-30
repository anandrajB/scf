from django.contrib import admin
from django.urls import path
from .views import BankSignupApiview, Countriesview, CurrenciesView , CustomerSignupApiview , PartiesSignupApiview , CustomerListApiview, UserLoginView

urlpatterns = [
    path('bank/', BankSignupApiview.as_view() ),
    path('Parties/', PartiesSignupApiview.as_view() ),
    path('customer/', CustomerSignupApiview.as_view() ),
    path('cust/', CustomerListApiview.as_view() ),
    path('currency/',CurrenciesView.as_view()),
    path('country/',Countriesview.as_view()),
    path('login/',UserLoginView.as_view())
]

