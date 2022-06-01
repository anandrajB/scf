from accounts.models import userprocessauth
from rest_framework import permissions


class Ismaker_invoice(permissions.BasePermission):
    def has_permission(self, request, view):
        qs = userprocessauth.objects.get(
            user=request.user, model='INVOICE',  action__desc__contains='SUBMIT')
        if qs.data_entry == True:
            return True


class IsSign_A_invoice(permissions.BasePermission):
    def has_permission(self, request, view):
        qs = userprocessauth.objects.get(
            user=request.user, model='INVOICE', action__desc__contains="SUBMIT")
        if qs.sign_a == True:
            return True


class IsSign_B_invoice(permissions.BasePermission):
    def has_permission(self, request, view):
        qs = userprocessauth.objects.get(
            user=request.user, model='INVOICE',  action__desc__contains="SUBMIT")
        if qs.sign_b == True:
            return True


class Is_Sign_C_invoice(permissions.BasePermission):
    def has_permission(self, request, view):
        qs = userprocessauth.objects.get(
            user=request.user, model='INVOICE',  action__desc__contains="SUBMIT")
        if qs.sign_c == True:
            return True