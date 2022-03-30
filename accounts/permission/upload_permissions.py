from accounts.models import userprocessauth
from rest_framework import permissions


class Ismaker_upload(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            qs = userprocessauth.objects.get(user=request.user, model='UPLOAD',  action__desc__contains='SUBMIT')
        except:
            return None
        if qs.data_entry == True:
            return True
        

class IsSign_A_upload(permissions.BasePermission):
    def has_permission(self, request, view):
        qs = userprocessauth.objects.get(
            user=request.user, model='UPLOAD', action__desc__contains="SUBMIT")
        if qs.sign_a == True:
            return True


class IsSign_B_upload(permissions.BasePermission):
    def has_permission(self, request, view):
        qs = userprocessauth.objects.get(
            user=request.user, model='UPLOAD',  action__desc__contains="SUBMIT")
        if qs.sign_b == True:
            return True


class Is_Sign_C_upload(permissions.BasePermission):
    def has_permission(self, request, view):
        qs = userprocessauth.objects.get(
            user=request.user, model='UPLOAD',  action__desc__contains="SUBMIT")
        if qs.sign_c == True:
            return True