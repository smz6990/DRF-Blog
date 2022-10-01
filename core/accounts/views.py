from django.contrib.auth import views
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.contrib.auth import authenticate
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import update_session_auth_hash
from mail_templated import EmailMessage
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import UserIsVerifiedMixin
from .models import Profile
from .forms import (
    CustomUserCreationForm,
    ProfileFrom,
    CustomAuthenticationForm,
    CustomPasswordChangeForm,
)
from .utils import EmailThreadSend


class CustomLoginView(views.LoginView):
    """
    Class that log in a user
    """

    form_class = CustomAuthenticationForm
    template_name = "accounts/login.html"

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        messages.success(self.request, "You successfully logged in.")
        return super().form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.error(self.request, "Something went wrong.")
        messages.error(self.request, form.errors)
        return super().form_invalid(form)


class CustomLogoutView(LoginRequiredMixin, views.LogoutView):
    """
    Class that log out a user
    """

    template_name = "blank.html"


class CustomSignUpView(CreateView):
    """
    Class that sign up a user
    """

    form_class = CustomUserCreationForm
    template_name = "accounts/signup.html"

    def form_valid(self, form):
        """
        If the form is valid, save the associated model,
        and send verification email.
        """
        self.object = form.save()
        valid = super(CustomSignUpView, self).form_valid(form)
        email = self.request.POST["email"]
        password = self.request.POST["password1"]
        user = authenticate(self.request, email=email, password=password)
        token = str(AccessToken.for_user(user))
        message = EmailMessage(
            "email/email-verification.tpl",
            {"token": token, "user": user},
            "info@test.com",
            to=[email],
        )
        EmailThreadSend(message).start()

        messages.success(
            self.request, "Your account successfully created."
        )
        messages.success(
            self.request, "Verification email is send to your email."
        )
        return valid

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.error(self.request, "Something went wrong")
        messages.error(self.request, form.errors)
        return super().form_invalid(form)


class ProfileUpdateView(
    LoginRequiredMixin, UserIsVerifiedMixin, UpdateView
):
    """
    Class to update Profile of a user
    """

    context_object_name = "profile"
    form_class = ProfileFrom
    model = Profile
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        user = self.request.user
        profile = Profile.objects.get(user__email=user)
        data["profile"] = profile
        return data

    def get(self, request, *args, **kwargs):
        """
        Only the owner of profile have access to profile
        """
        self.object = self.get_object()
        if self.object.user != request.user:
            messages.error(request, "You can not see this profile.")
            return HttpResponseRedirect(reverse("website:index"))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Only the owner of profile have access to profile
        """
        self.object = self.get_object()
        if self.object.user != request.user:
            messages.error(request, "You can not see this profile.")
            return HttpResponseRedirect(reverse("website:index"))
        return super().post(request, *args, **kwargs)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.error(self.request, "Something went wrong.")
        messages.error(self.request, form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        form.instance.user = self.request.user
        messages.success(
            self.request, "Your Profile updated successfully."
        )
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.request.user.id
        return reverse("accounts:profile", kwargs={"pk": pk})


class CustomChangePasswordView(
    LoginRequiredMixin, UserIsVerifiedMixin, views.PasswordChangeView
):
    """
    Customizing the ChangePasswordView
    """

    form_class = CustomPasswordChangeForm
    success_url = "/"
    template_name = "accounts/change-password.html"

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        messages.success(self.request, "Your password change successfully")
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong!")
        messages.error(self.request, form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        pk = self.request.user.id
        return reverse("accounts:profile", kwargs={"pk": pk})


def password_reset_request_view(request):
    pass
