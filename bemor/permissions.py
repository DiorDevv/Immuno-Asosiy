from rest_framework.permissions import BasePermission


class BemorPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.role_user == "VRACH":
            return True

        if view.action == 'create':
            return False

        return True

