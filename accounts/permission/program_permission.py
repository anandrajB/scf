# PROGRAM PERMISSIONS 
from urllib import request
from rest_framework import permissions
from accounts.models import userprocessauth
from accounts.models import User
# from rest_framework


def is_uploader(self, user):
        return ((not user.is_superuser) and user.is_authenticated)


def is_approver(self, user):
    return (user.is_superuser and user.is_authenticated)




#MAKER AND SUBMIT SIGN PERMISSIONS 

class Ismaker(permissions.BasePermission):
    def has_permission(self, request, view):
        qs = userprocessauth.objects.get(user = request.user ,model = 'PROGRAM',  action__desc__contains = 'SUBMIT')
        return True
        
    

class IsSign_A(permissions.BasePermission):
    def has_permission(self, request, view):
        qs = userprocessauth.objects.get(user = request.user , model = 'PROGRAM', action__desc__contains = "SUBMIT")
        if qs.sign_a == True:
            return True


class IsSign_B(permissions.BasePermission):
    def has_permission(self, request, view):
        qs = userprocessauth.objects.get(user = request.user ,model = 'PROGRAM',  action__desc__contains = "SUBMIT")
        if qs.sign_b == True:
            return True

class Is_Sign_C(permissions.BasePermission):
    def has_permission(self, request, view):
        qs = userprocessauth.objects.get(user = request.user ,model = 'PROGRAM',  action__desc__contains = "SUBMIT")
        if qs.sign_c == True:
            return True





# REJECT PERMISSION FOR BANK USER 

class Is_Rejecter(permissions.BasePermission):
    def has_permission(self, request, view):
        try : 
            qs = userprocessauth.objects.get(user = request.user ,model = 'PROGRAM',  action__desc__contains = 'REJECT')
            return True
        except:
            return False


class IsReject_Sign_A(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        qs = userprocessauth.objects.get(user = user ,model = 'PROGRAM',  action__desc__contains = "REJECT")
        if qs.sign_a == True | user.is_administrator == True:
            return True


class IsReject_Sign_B(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        qs = userprocessauth.objects.get(user = user  , model = 'PROGRAM', action__desc__contains = "REJECT")
        if qs.sign_b == True | user.is_administrator == True:
            return True


class IsReject_Sign_C(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        qs = userprocessauth.objects.get(user = user  ,model = 'PROGRAM',  action__desc__contains = "REJECT")
        if qs.sign_c == True and user.is_administrator == True:
            return True


# ACCEPT PERMISSIONS

class Is_Accepter(permissions.BasePermission):
    def has_permission(self, request, view):
        try : 
            qs = userprocessauth.objects.get(user = request.user ,model = 'PROGRAM',  action__desc__contains = 'ACCEPT')
            return True
        except:
            return False


class IsAccept_Sign_A(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        qs = userprocessauth.objects.get(user = user  , model = 'PROGRAM', action__desc__contains = "ACCEPT")
        if qs.sign_a == True :
            return True


class IsAccept_Sign_B(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        qs = userprocessauth.objects.get(user = user  ,  model = 'PROGRAM',action__desc__contains = "ACCEPT")
        if qs.sign_b == True :
            return True


class IsAccept_Sign_C(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        qs = userprocessauth.objects.get(user = user  , model = 'PROGRAM', action__desc__contains = "ACCEPT")
        if qs.sign_c == True :
            return True



# APPROVE PERMISSIONS  -  bank user

class Is_Approve(permissions.BasePermission):
    def has_permission(self, request, view):
        try : 
            qs = userprocessauth.objects.get(user = request.user ,model = 'PROGRAM',  action__desc__contains = 'APPROVE')
            return True
        except:
            return False


class IsApprove_Sign_A(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        qs = userprocessauth.objects.get(user = user  , model = 'PROGRAM', action__desc__contains = "APPROVE")
        if qs.sign_a == True and user.party.party_type == "BANK":
            return True


class IsApprove_Sign_B(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        qs = userprocessauth.objects.get(user = user  ,  model = 'PROGRAM',action__desc__contains = "APPROVE")
        if qs.sign_b == True and user.party.party_type == "BANK":
            return True


class IsApprove_Sign_C(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        qs = userprocessauth.objects.get(user = user  , model = 'PROGRAM', action__desc__contains = "APPROVE")
        if qs.sign_c == True and user.party.party_type == "BANK":
            return True
