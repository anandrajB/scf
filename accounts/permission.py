from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser


# SUPERUSER / ADMIN (bank)
class Is_Administrator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_administrator == True:
            return True

