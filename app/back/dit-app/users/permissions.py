from http import HTTPMethod
from rest_framework.permissions import BasePermission


class UserPermissions(BasePermission):
    def has_permission(self, request, view):
        is_authenticated = request.user.is_authenticated
        return any([
            not is_authenticated and request.method == HTTPMethod.POST.name,
            is_authenticated and request.method != HTTPMethod.POST.name
        ])