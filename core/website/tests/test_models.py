import pytest

from ..models import Newsletter, Contact


@pytest.mark.django_db
class TestNewsletterModel:
    def test_newsletter_model_valid_data(self):
        data = {"email": "test@test.com"}
        model_obj = Newsletter.objects.create(**data)
        model_obj.save()
        assert (
            Newsletter.objects.filter(email=model_obj.email).exists()
            is True
        )
        assert model_obj.email == data["email"]


@pytest.mark.django_db
class TestContactModel:
    def test_contact_model_valid_data(self):
        data = {
            "name": "test",
            "email": "test@test.com",
            "subject": "test subject",
            "message": "test message",
        }
        contact_obj = Contact.objects.create(**data)
        contact_obj.save()
        assert Contact.objects.count() == 1
        assert contact_obj.name == "test"
