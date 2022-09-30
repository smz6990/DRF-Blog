from django.forms import ModelForm

from simplemathcaptcha.fields import MathCaptchaField

from .models import Newsletter, Contact


class NewsletterForm(ModelForm):
    """Class that create a form for Newsletter model"""

    class Meta:
        model = Newsletter
        fields = "__all__"


class ContactForm(ModelForm):
    """Class that create a form for Contact model"""

    captcha = MathCaptchaField()

    class Meta:
        model = Contact
        fields = ["name", "email", "subject", "message", "captcha"]
