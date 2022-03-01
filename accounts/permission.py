from rest_framework import permissions



# SUPERUSER / ADMIN (bank)
class Is_Administrator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_administrator == True:
            return True