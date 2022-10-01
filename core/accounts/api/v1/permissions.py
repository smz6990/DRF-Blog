from rest_framework import permissions


class NotAuthenticated(permissions.BasePermission):
    """
    Base permission to NOT allow access to authenticated users.
    """

    def has_permission(self, request, view):
        """
        Reject authenticated user
        """

        return not bool(request.user and request.user.is_authenticated)


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owner of Profile
    access to their profile page.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        return obj.user == request.user


class IsVerifyOrReadOnly(permissions.BasePermission):
    """
    Base permission class that only allow verified user.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_authenticated:
            return request.user.is_verify
        return False
