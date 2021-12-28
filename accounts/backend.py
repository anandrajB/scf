from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
User = get_user_model()


class AuthenticationBackend(ModelBackend):
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(Q(email__iexact=username) | Q(phone__iexact=username))
            print('...')
            print('test working')
            if(user.check_password(password)):
                return user
        except User.DoesNotExist:
            pass
