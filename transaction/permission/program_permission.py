# PROGRAM PERMISSIONS 
from urllib import request
from rest_framework import permissions
import accounts


def is_uploader(self, user):
        return ((not user.is_superuser) and user.is_authenticated)


def is_approver(self, user):
    return (user.is_superuser and user.is_authenticated)


# SUPERUSER / ADMIN 
class Is_administrator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_administrator == True:
            return True


#MAKER AND SUBMIT SIGN PERMISSIONS 

class Ismaker(permissions.BasePermission):
    def has_permission(self, request, view):
        qs = accounts.models.userprocessauth.objects.get(user = request.user ,model = 'PROGRAM',  action__desc__contains = 'SUBMIT')
        if qs.data_entry == True:
            return True


class IsSign_A(permissions.BasePermission):
    def has_permission(self, request, view):
        qs = accounts.models.userprocessauth.objects.get(user = request.user , model = 'PROGRAM', action__desc__contains = "SUBMIT")
        if qs.sign_a == True:
            return True


class IsSign_B(permissions.BasePermission):
    def has_permission(self, request, view):
        qs = accounts.models.userprocessauth.objects.get(user = request.user ,model = 'PROGRAM',  action__desc__contains = "SUBMIT")
        if qs.sign_b == True:
            return True

class Is_Sign_C(permissions.BasePermission):
    def has_permission(self, request, view):
        qs = accounts.models.userprocessauth.objects.get(user = request.user ,model = 'PROGRAM',  action__desc__contains = "SUBMIT")
        if qs.sign_c == True:
            return True



# REJECT PERMISSION 

class Is_Rejecter(permissions.BasePermission):
    def has_permission(self, request, view):
        qs = accounts.models.userprocessauth.objects.get(user = request.user , model = 'PROGRAM', action__desc__contains = "REJECT")
        if qs.data_entry == True:
            return True


class IsReject_Sign_A(permissions.BasePermission):
    def has_permission(self, request, view):
        qs = accounts.models.userprocessauth.objects.get(user = request.user ,model = 'PROGRAM',  action__desc__contains = "REJECT")
        if qs.sign_a == True:
            return True


class IsReject_Sign_B(permissions.BasePermission):
    def has_permission(self, request, view):
        qs = accounts.models.userprocessauth.objects.get(user = request.user , model = 'PROGRAM', action__desc__contains = "REJECT")
        if qs.sign_b == True:
            return True


class IsReject_Sign_C(permissions.BasePermission):
    def has_permission(self, request, view):
        qs = accounts.models.userprocessauth.objects.get(user = request.user ,model = 'PROGRAM',  action__desc__contains = "REJECT")
        if qs.sign_c == True:
            return True


# APPROVE PERMISSIONS

class Is_Accepter(permissions.BasePermission):
    def has_permission(self, request, view):
        qs = accounts.models.userprocessauth.objects.get(user = request.user , model = 'PROGRAM', action__desc__contains = "ACCEPT")
        if qs.data_entry == True:
            return True


class IsAccept_Sign_A(permissions.BasePermission):
    def has_permission(self, request, view):
        qs = accounts.models.userprocessauth.objects.get(user = request.user , model = 'PROGRAM', action__desc__contains = "ACCEPT")
        if qs.sign_a == True:
            return True


class IsAccept_Sign_B(permissions.BasePermission):
    def has_permission(self, request, view):
        qs = accounts.models.userprocessauth.objects.get(user = request.user ,  model = 'PROGRAM',action__desc__contains = "ACCEPT")
        if qs.sign_b == True:
            return True


class IsAccept_Sign_C(permissions.BasePermission):
    def has_permission(self, request, view):
        qs = accounts.models.userprocessauth.objects.get(user = request.user , model = 'PROGRAM', action__desc__contains = "ACCEPT")
        if qs.sign_c == True:
            return True
