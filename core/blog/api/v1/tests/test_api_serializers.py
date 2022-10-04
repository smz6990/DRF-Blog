import pytest
from datetime import datetime

from ..serializers import (
    CategorySerializer,
    CustomUserSerializer,
    CommentSerializer,
    PostSerializer,
)


@pytest.mark.django_db
class TestBlogSerializers:
    def test_category_serializer_valid_data(self):
        data = {"name": "test"}
        serializer = CategorySerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data == data
        assert serializer.data == data
        assert serializer.errors == {}

    def test_category_serializer_invalid_data(self):
        data = {}
        serializer = CategorySerializer(data=data)
        assert not serializer.is_valid()
        assert serializer.validated_data == data
        assert serializer.data == data

    def test_custom_user_serializer_valid_data(self):
        data = {"email": "test@test.com"}
        serializer = CustomUserSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data == data
        assert serializer.data == data
        assert serializer.errors == {}

    def test_custom_user_serializer_invalid_data(self):
        data = {}
        serializer = CustomUserSerializer(data=data)
        assert not serializer.is_valid()
        assert serializer.validated_data == data
        assert serializer.data == data

    def test_comment_serializer_valid_data(self):
        data = {
            "name": "test",
            "email": "test@test.com",
            "message": "test message",
            "created_date": datetime.now(),
        }
        serializer = CommentSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.errors == {}

    def test_comment_serializer_invalid_data(self):
        data = {}
        serializer = CommentSerializer(data=data)
        assert not serializer.is_valid()
        assert serializer.validated_data == data
        assert serializer.data == data

    def test_post_serializer_valid_data(self):
        data = {
            "title": "test title",
            "content": "test content",
            "published_date": datetime.now(),
        }
        serializer = PostSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.errors == {}

    def test_post_serializer_invalid_data(self):
        data = {}
        serializer = PostSerializer(data=data)
        assert not serializer.is_valid()
        assert serializer.validated_data == data
        assert serializer.data == data
