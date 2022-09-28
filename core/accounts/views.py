from django.contrib.auth import views
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import Profile
from .forms import (
    CustomUserCreationForm,
    ProfileFrom,
    CustomAuthenticationForm,
)


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
        """If the form is valid, save the associated model."""
        self.object = form.save()
        valid = super(CustomSignUpView, self).form_valid(form)
        email = self.request.POST["email"]
        password = self.request.POST["password1"]
        user = authenticate(self.request, email=email, password=password)
        login(self.request, user)
        messages.success(self.request, "You account successfully created.")
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


def password_reset_request_view(request):
    pass
