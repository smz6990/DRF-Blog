from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User,Profile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    creating a class to show the User fields in admin panel
    """
    model = User
    list_display = ['email','is_superuser','is_staff','is_active']
    list_filter = ['email','is_superuser','is_staff','is_active']
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser')}
        ),
    )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
        creating a class to show the Profile fields in admin panel
    """
    list_display = ['first_name','last_name','user','created_date','updated_date']
    search_fields = ['first_name','last_name','user']
    ordering = ['created_date']