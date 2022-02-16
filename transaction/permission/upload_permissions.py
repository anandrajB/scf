from rest_framework import permissions
import accounts


class Ismaker(permissions.BasePermission):
    def has_permission(self, request, view):
        qs = accounts.models.userprocessauth.objects.get(user = request.user ,model = 'UPLOAD',  action__desc__contains = 'SUBMIT')
        if qs.data_entry == True:
            return True


class IsSign_A(permissions.BasePermission):
    def has_permission(self, request, view):
        qs = accounts.models.userprocessauth.objects.get(user = request.user , model = 'UPLOAD', action__desc__contains = "SUBMIT")
        if qs.sign_a == True:
            return True


class IsSign_B(permissions.BasePermission):
    def has_permission(self, request, view):
        qs = accounts.models.userprocessauth.objects.get(user = request.user ,model = 'UPLOAD',  action__desc__contains = "SUBMIT")
        if qs.sign_b == True:
            return True

class Is_Sign_C(permissions.BasePermission):
    def has_permission(self, request, view):
        qs = accounts.models.userprocessauth.objects.get(user = request.user ,model = 'UPLOAD',  action__desc__contains = "SUBMIT")
        if qs.sign_c == True:
            return True