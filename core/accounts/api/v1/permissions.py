from rest_framework import permissions


class NotAuthenticated(permissions.BasePermission):
    """
    Do NOT allow access to authenticated users.
    """

    def has_permission(self, request, view):
        """
        Reject authenticated user
        """

        return not bool(request.user and request.user.is_authenticated)
