from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages


class UserIsVerifiedMixin(AccessMixin):
    """Verify that the current user is verified."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_verify:
            messages.warning(
                request, "Please Verify your account to access this page"
            )
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
