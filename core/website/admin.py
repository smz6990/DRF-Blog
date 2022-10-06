from django.contrib import admin

from .models import Contact, Newsletter


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Class that show Contact model in admin panel"""

    list_display = ["name", "email", "subject", "created_date"]
    list_filter = ["email", "subject"]
    search_fields = ["name", "email", "subject", "message"]


admin.site.register(Newsletter)
