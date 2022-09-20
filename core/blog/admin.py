from django.contrib import admin
from blog.models import Category, Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    creating class to modify the admin panel for Post model
    """
    date_hierarchy = 'created_date'
    list_display = [
        'author', 'title', 'status',
        'published_date', 'created_date',
        ]
    list_filter = ['author', 'status', 'category']
    search_fields = ['title', 'content']
    
    
# registering the Category model to show it in admin panel
admin.site.register(Category)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Creating admin panel for Comment model
    """
    date_hierarchy = 'created_date'
    list_display = [
        'post', 'email',
        'created_date'
        ]
    list_filter = ['post']
    search_fields = ['post', 'email', 'message']