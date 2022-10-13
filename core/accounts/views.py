from django.contrib.auth import views
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, View, FormView
from django.contrib.auth import authenticate
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth import update_session_auth_hash
from mail_templated import EmailMessage
from rest_framework_simplejwt.tokens import AccessToken
import jwt
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from .permissions import UserIsVerifiedMixin, NotAuthenticatedUserMixin
from .models import Profile, User
from .forms import (
    CustomUserCreationForm,
    ProfileFrom,
    CustomAuthenticationForm,
    CustomPasswordChangeForm,
    ResendVerifyEmailForm,
    CustomPasswordResetForm,
    ReSetPasswordForm,
)
from .utils import EmailThreadSend


class CustomLoginView(NotAuthenticatedUserMixin, views.LoginView):
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


class CustomSignUpView(NotAuthenticatedUserMixin, CreateView):
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
            "noreply@salehmzh.ir",
            to=[email],
        )
        EmailThreadSend(message).start()

        messages.success(self.request, "Your account successfully created.")
        messages.success(
            self.request, "Verification email is send to your email."
        )
        return valid

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.error(self.request, "Something went wrong")
        messages.error(self.request, form.errors)
        return super().form_invalid(form)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
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
            messages.error(
                request, "You dont have permissions to see this page."
            )
            return HttpResponseRedirect(reverse("website:index"))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Only the owner of profile have access to profile
        """
        self.object = self.get_object()
        if self.object.user != request.user:
            messages.error(
                request, "You dont have permissions to see this page."
            )
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
        messages.success(self.request, "Your Profile updated successfully.")
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
    success_url = reverse_lazy("accounts:login")
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


class VerifyEmailView(View):
    """
    View to verify user by given email
    """

    def get(self, request, *args, **kwargs):
        token = kwargs.get("token")
        try:
            payload = jwt.decode(
                jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"]
            )
            user = User.objects.get(id=payload["user_id"])
            if not user.is_verify:
                user.is_verify = True
                user.save()
                messages.success(request, "Your email is verified!")
                return redirect(
                    reverse("accounts:profile", kwargs={"pk": user.id})
                )
            else:
                messages.info(
                    request, "Your email has already been verified!"
                )
                return redirect(
                    reverse("accounts:profile", kwargs={"pk": user.id})
                )
        except jwt.ExpiredSignatureError:
            messages.error(request, "Activations link expired")
            return redirect(reverse("accounts:resend-verify-email"))
        except jwt.exceptions.DecodeError:
            messages.error(request, "Invalid Token")
            return redirect(reverse("accounts:resend-verify-email"))


class ResendVerifyEmailView(FormView):
    """
    View to resend verification email
    """

    form_class = ResendVerifyEmailForm
    template_name = "accounts/email-verify-resend.html"

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(
                self.request, "User with the given email does not exist!"
            )
            return redirect(reverse("accounts:resend-verify-email"))
        if user.is_verify:
            messages.info(
                self.request, "Your account has been already verified!"
            )
            return redirect(
                reverse("accounts:profile", kwargs={"pk": user.id})
            )
        token = str(AccessToken.for_user(user))
        message = EmailMessage(
            "email/email-verification.tpl",
            {"token": token, "user": user},
            "noreply@salehmzh.ir",
            to=[email],
        )
        EmailThreadSend(message).start()
        messages.success(self.request, "Verification email is sent to you!")
        return redirect("/")

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)


class PasswordResetSend(FormView):
    """
    View to send email to reset password.
    """

    form_class = CustomPasswordResetForm
    template_name = "accounts/password_reset.html"

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(
                self.request, "User with the given email does not exist!"
            )
            return redirect(reverse("accounts:password_reset"))
        token = str(AccessToken.for_user(user))
        message = EmailMessage(
            "email/reset-password.tpl",
            {"token": token, "user": user},
            "noreply@salehmzh.ir",
            to=[email],
        )
        EmailThreadSend(message).start()
        messages.success(
            self.request, "reset password email is sent to your inbox!"
        )
        return redirect("/")

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)


class PasswordResetDoneView(FormView):
    """
    View to set new password for user without old password
    """

    success_url = reverse_lazy("accounts:login")
    form_class = ReSetPasswordForm
    template_name = "accounts/password_reset_confirm.html"

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        self.token = kwargs.get("token")
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.token = kwargs.get("token")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        request = self.request
        token = self.token
        try:
            payload = jwt.decode(
                jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"]
            )
            user = User.objects.get(id=payload["user_id"])
            password = form.data.get("new_password")
            user.set_password(password)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password changed successfully!")
            messages.success(request, f"'{user}', please login!")
        except jwt.ExpiredSignatureError:
            messages.error(request, "Activations link expired")
            return redirect(reverse("accounts:resend-verify-email"))
        except jwt.exceptions.DecodeError:
            messages.error(request, "Invalid Token")
            return redirect(reverse("accounts:resend-verify-email"))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)
