import pytest

from ..forms import ContactForm, NewsletterForm
from ..models import Newsletter


@pytest.mark.django_db
class TestNewsletterForm:
    def test_newsletter_form_valid_data(self):
        data = {"email": "test@test.com"}
        form = NewsletterForm(data)
        assert form.is_valid() is True
        assert len(form.errors) == 0

    def test_newsletter_form_invalid_data(self):
        data = {"email": "test"}
        form = NewsletterForm(data)
        assert form.is_valid() is False
        assert len(form.errors) == 1
        assert form.has_error("email") is True

    def test_newsletter_form_no_data(self):
        form = NewsletterForm()
        assert form.is_valid() is False

    def test_newsletter_form_save_in_database(self):
        data = {"email": "test@test.com"}
        form = NewsletterForm(data)
        form.save()
        assert form.is_valid() is True
        assert len(form.errors) == 0
        assert (
            Newsletter.objects.filter(email=data["email"]).exists() is True
        )


class TestContactForm:
    def test_contact_form_valid_data(self):
        data = {
            "name": "test",
            "email": "test@test.com",
            "subject": "test subject",
            "message": "test message",
            "captcha": 1,
        }
        form = ContactForm(data)
        # its False because captcha field is incorrect
        assert form.is_valid() is False
        assert len(form.errors) == 1
        assert form.has_error("captcha") is True

    def test_contact_form_invalid_data(self):
        data = {
            "name": "test",
            "email": "invalid email format",
            "subject": "test subject",
            "message": "test message",
            "captcha": 1,
        }
        form = ContactForm(data)
        assert form.is_valid() is False
        assert len(form.errors) == 2

    def test_contact_form_missing_field_data(self):
        data = {
            "name": "test",
            "message": "test message",
        }
        form = ContactForm(data)
        assert form.is_valid() is False
        assert len(form.errors) == 3

    def test_contact_form_no_data(self):
        form = ContactForm()
        assert form.is_valid() is False
