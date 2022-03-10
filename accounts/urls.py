from django.contrib import admin
from django.urls import path
from .views import (
    ActionUpdateDeleteApiview,
    BankCreateApiview,
    CountriesApiView,
    CurrenciesView,
    ModelApiview,
    ModelUpdateDeleteApiview,
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
    UserProcessAuthView,
    UserProcessAuthUpdateApiview,
    ActionApiview,
    PartyDetailsUpdateDeleteApiview,
    Inactiveuser
)

urlpatterns = [
    path('bank/', BankCreateApiview.as_view() ),
    path('party/', PartiesSignupApiview.as_view() ),
    path('party/<int:pk>/',PartyDetailsUpdateDeleteApiview.as_view()),
    path('signup/', UserSignUpApiView.as_view() ,name='user-signup' ),
    path('login/',UserLoginView.as_view()),
    path('logout/',UserLogoutView.as_view()),
    path('otp/',OtpSendApi.as_view(),name='OTP-generate'),
    path('otp-v/',OtpVerifyLoginApiview.as_view(),name='OTP-verify and login'),
    path('user/', UserListApiview.as_view() , name = 'user-list' ),
    path('user/<int:pk>/',UserDetailsUpdateDeleteApiview.as_view(),name='user-detail-pk'),
    path('inactive_user',Inactiveuser.as_view(),name='inactive-user-list'),
    path('currency/',CurrenciesView.as_view()),
    path('currency/<int:pk>/',CurrenciesUpdateDeleteApiview.as_view()),
    path('country/',CountriesApiView.as_view()),
    path('country/<int:pk>/',CountryUpdateDeleteApiview.as_view()),
    path('userprocess/',UserProcessAuthView.as_view()),
    path('userprocess/<int:pk>/',UserProcessAuthUpdateApiview.as_view()),
    path('signatures/<int:pk>/',SignaturesUpdateDeleteApiview.as_view()),
    path('signatures/',SignaturesCreateApiView.as_view()),
    path('action/',ActionApiview.as_view()),
    path('action/<int:pk>/',ActionUpdateDeleteApiview.as_view()),
    path('models/',ModelApiview.as_view()),
    path('models/<int:pk>/',ModelUpdateDeleteApiview.as_view())
]

