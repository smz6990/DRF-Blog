from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages


class UserIsVerifiedMixin(AccessMixin):
    """Allowed current user if user is verified."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_verify:
            self.permission_denied_message = (
                "Please Verify your account to access this page"
            )
            messages.warning(
                request, "Please Verify your account to access this page"
            )
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class NotAuthenticatedUserMixin(AccessMixin):
    """Only accepts Not authenticated user."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.permission_denied_message = (
                f"{request.user}, you Dont have access to this page!"
            )
            messages.warning(
                request,
                f"{request.user}, you Dont have access to this page",
            )
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
