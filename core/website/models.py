from django.db import models


class Newsletter(models.Model):
    """Model for Newsletter form"""

    email = models.EmailField()

    def __str__(self):
        return self.email


class Contact(models.Model):
    """Model for Contact form"""

    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return self.email
