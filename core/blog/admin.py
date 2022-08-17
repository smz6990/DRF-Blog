from django.contrib import admin
from blog.models import Category,Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    creating class to modify the admin panel
    """
    date_hierarchy = 'created_date'
    list_display = ['author', 'title', 'status', 'category', 'published_date', 'created_date']
    list_filter = ['author', 'status', 'category']
    search_fields = ['author', 'title', 'content']
    
    
# registering the Category model to show it in admin panel
admin.site.register(Category)
