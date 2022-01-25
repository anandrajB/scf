from django.contrib import admin
from django.urls import path
from .views import (
    BankCreateApiview,
    Countriesview,
    CurrenciesView,
    SignaturesCreateApiView,
    UserListApiview,
    UserProcessView,
    UserSignUpApiView ,
    PartiesSignupApiview ,
    UserLoginView,
    UserDetailsUpdateDeleteApiview,
    UserLogoutView
)

urlpatterns = [
    path('bank/', BankCreateApiview.as_view() ),
    path('party/', PartiesSignupApiview.as_view() ),
    path('signup/', UserSignUpApiView.as_view() ,name='user-signup' ),
    path('user/', UserListApiview.as_view() , name = 'user-list' ),
    path('user/<int:pk>/',UserDetailsUpdateDeleteApiview.as_view(),name='user-detail-pk'),
    path('currency/',CurrenciesView.as_view()),
    path('country/',Countriesview.as_view()),
    path('login/',UserLoginView.as_view()),
    path('logout/',UserLogoutView.as_view()),
    path('userprocess/',UserProcessView.as_view()),
    path('signatures/',SignaturesCreateApiView.as_view())
    
]

