from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser


# BANK USER

class Is_BankAdministrator(permissions.BasePermission):
    def has_permission(self, request, view):
            return bool(request.user.is_administrator == True and request.user.party.party_type == "BANK")


# ADMINISTRATOR USER 

class Is_Administrator(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_administrator == True)


# ADMINISTRATOR USER FOR PARTY 

class Is_PartyAdministrator(permissions.BasePermission):
    def has_permission(self, request,view):
        user = request.user
        party_type = user.party.party_type
        if user.is_administrator == True and (party_type == "CUSTOMER" | party_type == "SELLER" | party_type == "BUYER"):
            return True


# BUYER USER 

class Is_Buyer(permissions.BasePermission):
    def has_permission(self,request,view):
        return bool(request.user.party.party_type == "BUYER")

# SELLER 

class Is_Seller(permissions.BasePermission):
    def has_permission(self,request,view):
        return bool(request.user.party.party_type == "SELLER")


# BANK USER 

class Is_Bank(permissions.BasePermission):
    def has_permission(self,request,view):
        return bool(request.user.party.party_type == "BANK")


