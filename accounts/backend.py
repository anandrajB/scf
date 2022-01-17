from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
User = get_user_model()

# CUSTOM BACKEND FOR PASSWORDLESS AUTH

class AuthenticationBackend(ModelBackend):
    def authenticate(self, request , phone = None,email=None):
        try:
            return User.objects.get(phone = phone,email=email)
        except User.DoesNotExist:
            return None


    def get_user(self, user_id):
        try: 
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

