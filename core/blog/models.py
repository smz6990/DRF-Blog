from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField 
from accounts.models import Profile


class Post(models.Model):
    """
    This is a table in our DB, Post is table name and below
    attributes are our field in our table.
    """
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    content = RichTextUploadingField()
    status = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True,
        upload_to="blog/post_pics/", default="blog/post_pics/default.jpg"
    )
    category = models.ManyToManyField("Category", null=True, blank=True)
    published_date = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_date", "-created_date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:single", kwargs={"pk": self.id})


class Category(models.Model):
    """This is the Category table with name field in our database."""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Comment(models.Model):
    """
    Class that represent the comment section of each Post.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField()
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-updated_date"]

    def __str__(self):
        return "{} on {}".format(self.email, self.post.title)

    def get_absolute_url(self):
        return reverse("blog:single", kwargs={"pk": self.post.id})