# PROGRAM PERMISSIONS 
from urllib import request
from rest_framework import permissions
import accounts
from accounts.models import User
# from rest_framework


def is_uploader(self, user):
        return ((not user.is_superuser) and user.is_authenticated)


def is_approver(self, user):
    return (user.is_superuser and user.is_authenticated)


# # SUPERUSER / ADMIN 
# class Is_administrator(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.user.is_administrator == True:
#             return True


#MAKER AND SUBMIT SIGN PERMISSIONS 

class Ismaker(permissions.BasePermission):
    def has_permission(self, request, view):
        try : 
            qs = accounts.models.userprocessauth.objects.get(user = request.user ,model = 'PROGRAM',  action__desc__contains = 'SUBMIT')
            if qs.data_entry == True:
                return True
        except:
            return False
    

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





# REJECT PERMISSION FOR BANK USER 

class Is_Rejecter(permissions.BasePermission):
    def has_permission(self, request, view):
        user = User.objects.get(is_administrator = True)
        qs = accounts.models.userprocessauth.objects.get(user = user , model = 'PROGRAM', action__desc__contains = "REJECT")
        if qs.data_entry == True:
            return True


class IsReject_Sign_A(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        qs = accounts.models.userprocessauth.objects.get(user = request.user ,model = 'PROGRAM',  action__desc__contains = "REJECT")
        if qs.sign_a == True | user.is_administrator == True:
            return True


class IsReject_Sign_B(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        qs = accounts.models.userprocessauth.objects.get(user = request.user , model = 'PROGRAM', action__desc__contains = "REJECT")
        if qs.sign_b == True | user.is_administrator == True:
            return True


class IsReject_Sign_C(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        qs = accounts.models.userprocessauth.objects.get(user = request.user ,model = 'PROGRAM',  action__desc__contains = "REJECT")
        if qs.sign_c == True and user.is_administrator == True:
            return True


# ACCEPT PERMISSIONS

class Is_Accepter(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        qs = accounts.models.userprocessauth.objects.get(user = request.user , model = 'PROGRAM', action__desc__contains = "ACCEPT")
        if qs.data_entry == True :
            return True


class IsAccept_Sign_A(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        qs = accounts.models.userprocessauth.objects.get(user = request.user , model = 'PROGRAM', action__desc__contains = "ACCEPT")
        if qs.sign_a == True :
            return True


class IsAccept_Sign_B(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        qs = accounts.models.userprocessauth.objects.get(user = request.user ,  model = 'PROGRAM',action__desc__contains = "ACCEPT")
        if qs.sign_b == True :
            return True


class IsAccept_Sign_C(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        qs = accounts.models.userprocessauth.objects.get(user = request.user , model = 'PROGRAM', action__desc__contains = "ACCEPT")
        if qs.sign_c == True :
            return True



# APPROVE PERMISSIONS

class Is_Approve(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        qs = accounts.models.userprocessauth.objects.get(user = request.user , model = 'PROGRAM', action__desc__contains = "APPROVE")
        if qs.data_entry == True and user.is_administrator == True:
            return True


class IsApprove_Sign_A(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        qs = accounts.models.userprocessauth.objects.get(user = request.user , model = 'PROGRAM', action__desc__contains = "APPROVE")
        if qs.sign_a == True and user.is_administrator == True:
            return True


class IsApprove_Sign_B(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        qs = accounts.models.userprocessauth.objects.get(user = request.user ,  model = 'PROGRAM',action__desc__contains = "APPROVE")
        if qs.sign_b == True and user.is_administrator == True:
            return True


class IsApprove_Sign_C(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        qs = accounts.models.userprocessauth.objects.get(user = request.user , model = 'PROGRAM', action__desc__contains = "APPROVE")
        if qs.sign_c == True and user.is_administrator == True:
            return True
