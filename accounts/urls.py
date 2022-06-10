from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
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
    UserProfileApiView
)

urlpatterns = [
    path('bank/', BankCreateApiview.as_view() ,name = 'bank-create-api' ),
    path('party/', PartiesSignupApiview.as_view()),
    path('party/<int:pk>/',PartyDetailsUpdateDeleteApiview.as_view()),
    path('signup/', UserSignUpApiView.as_view() ,name='user-signup'),
    path('login/',csrf_exempt(UserLoginView.as_view()),name = 'user-login'),
    path('logout/',UserLogoutView.as_view(),name='user-logout'),
    path('otp/',OtpSendApi.as_view(),name='OTP-generate'),
    path('otp-v/',OtpVerifyLoginApiview.as_view(),name='OTP-verify and login'),
    path('user/', UserListApiview.as_view() , name = 'user-list-manage-users' ),
    path('user/<int:pk>/',UserDetailsUpdateDeleteApiview.as_view(),name='user-detail-pk'),
    path('profile/',UserProfileApiView.as_view(),name='user-profile'),
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
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

