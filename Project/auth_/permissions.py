from rest_framework.permissions import IsAuthenticated
from utils.constants import Role_Guest, Role_Admin


class GuestPermission(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == Role_Guest


class AdminPermission(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == Role_Admin
