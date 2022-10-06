from django import forms

from simplemathcaptcha.fields import MathCaptchaField

from .models import Post, Comment, Category


class PostForm(forms.ModelForm):
    """
    Class for creating form for Post model.
    """

    captcha = MathCaptchaField()

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "image",
            "category",
            "published_date",
            "captcha",
        ]


class CommentForm(forms.ModelForm):
    """
    Class for creating form for Comment model.
    """

    class Meta:
        model = Comment
        fields = ["post", "name", "email", "message"]


class CategoryForm(forms.ModelForm):
    """
    Class for creating form for Category Model
    """

    captcha = MathCaptchaField()

    class Meta:
        model = Category
        fields = ["name"]
