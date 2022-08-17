from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from accounts.managers import UserManager

class User(AbstractBaseUser,PermissionsMixin):
    """
    Creating a class that represent the custom User model for
    authentication
    """
    
    email = models.EmailField(unique=True,max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    # is_verified = models.BooleanField(default=False)
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def __str__(self):
        return self.email