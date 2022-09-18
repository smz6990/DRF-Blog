from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from accounts.models import Profile

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    creating a class to show the User fields in admin panel.
    """
    model = User
    list_display = ["email", "is_superuser", "is_staff", "is_active"]
    list_filter = ["is_superuser", "is_staff", "is_active"]
    search_fields = ("email",)
    ordering = ("email",)
    save_on_top = True
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    ("is_staff",
                    "is_active",
                    "is_superuser"),
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    ("is_staff",
                    "is_active",
                    "is_superuser"),
                ),
            },
        ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    creating a class to show the Profile fields in admin panel
    """
    list_display = ["user", "first_name", "last_name", "created_date", "updated_date"]
    list_filter = ['created_date']
    search_fields = ["user", "first_name", "last_name"]
    fields = ['user', "first_name", "last_name", 'image', 'description']
    ordering = ["created_date"]
