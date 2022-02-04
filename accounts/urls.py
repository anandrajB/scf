from django.contrib import admin
from django.urls import path
from .views import (
    BankCreateApiview,
    CountriesApiView,
    CurrenciesView,
    SignatureList,
    SignaturesCreateApiView,
    CurrenciesUpdateDeleteApiview,
    CountryUpdateDeleteApiview,
    UserListApiview,
    UserSignUpApiView ,
    PartiesSignupApiview ,
    UserLoginView,
    UserDetailsUpdateDeleteApiview,
    UserLogoutView,
    OtpSendApi,
    OtpVerifyLoginApiview,
    SignaturesUpdateDeleteApiview,
    UserProcessView
)

urlpatterns = [
    path('bank/', BankCreateApiview.as_view() ),
    path('party/', PartiesSignupApiview.as_view() ),
    path('signup/', UserSignUpApiView.as_view() ,name='user-signup' ),
    path('login/',UserLoginView.as_view()),
    path('logout/',UserLogoutView.as_view()),
    path('otp/',OtpSendApi.as_view(),name='OTP-generate'),
    path('otp-v/',OtpVerifyLoginApiview.as_view(),name='OTP-verify and login'),
    path('user/', UserListApiview.as_view() , name = 'user-list' ),
    path('user/<int:pk>/',UserDetailsUpdateDeleteApiview.as_view(),name='user-detail-pk'),
    path('currency/',CurrenciesView.as_view()),
    path('currency/<int:pk>/',CurrenciesUpdateDeleteApiview.as_view()),
    path('country/',CountriesApiView.as_view()),
    path('country/<int:pk>/',CountryUpdateDeleteApiview.as_view()),
    path('userprocess/',UserProcessView.as_view()),
    path('signatures/<int:pk>/',SignaturesUpdateDeleteApiview.as_view()),
    path('signatures/',SignaturesCreateApiView.as_view()),
    path('signatures-list/',SignatureList.as_view())
    
]

