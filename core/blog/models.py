from django.db import models
from django.contrib.auth import get_user_model


# getting the user model object
User = get_user_model()

class Post(models.Model):
    """
    This is a table in our DB, Post is table name and below attributes are our field in our table
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    content = models.TextField()
    status = models.BooleanField(default=False)
    image = models.ImageField(blank=True,null=True)
    category = models.ForeignKey('Category',on_delete=models.SET_NULL,null=True)
    published_date = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta: 
        ordering = ['-published_date','-created_date']
        
    def __str__(self):
        return self.title
    
class Category(models.Model):
    """
    This is the Category table with name field in our database
    """
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name