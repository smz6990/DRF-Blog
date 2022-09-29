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


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow ONLY owner of Profile
    access to their profile page
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        return obj.user == request.user
