import pytest

from ..models import Newsletter, Contact


@pytest.mark.django_db
class TestNewsletterModel:
    def test_newsletter_model_valid_data(self):
        data = {"email": "test@test.com"}
        model_obj = Newsletter.objects.create(**data)
        model_obj.save()
        assert Newsletter.objects.filter(email="test@test.com").exists()
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
        assert Contact.objects.filter(name="test").exists()
        assert contact_obj.name == "test"
        assert contact_obj.email == "test@test.com"
        assert contact_obj.subject == "test subject"
        assert contact_obj.message == "test message"
