from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from rest_framework.authtoken.models import Token

from accounts.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Creating a class that represent the custom User model for
    authentication.
    """

    email = models.EmailField(unique=True, max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_verify = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse("accounts:profile", kwargs={"pk": self.id})


class Profile(models.Model):
    """
    This is a class that represent the profile for every account
    in our project.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to="accounts/avatars/",
        default="accounts/avatars/default.jpg",
    )
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

    def get_absolute_url(self):
        return reverse("accounts:profile", kwargs={"pk": self.user.id})


@receiver(post_save, sender=User)
def save_profile_create_token(sender, instance, created, **kwargs):
    """
    A signal that create Profile for user when signing up
    """
    if created:
        Profile.objects.create(user=instance)
        Token.objects.create(user=instance)
