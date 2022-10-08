from django.utils.timezone import now
from rest_framework import serializers

from ...models import Post, Category, Comment
from accounts.models import Profile, User


class CategorySerializer(serializers.ModelSerializer):
    """
    Class that serialize the Category model
    """

    class Meta:
        model = Category
        fields = ["id", "name"]


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Class to serialize the user(author)
    """

    class Meta:
        model = User
        fields = ["id", "email"]


class CommentSerializer(serializers.ModelSerializer):
    """
    Class that serialize Comment
    """

    class Meta:
        model = Comment
        fields = ["name", "email", "message", "created_date"]


class PostSerializer(serializers.ModelSerializer):
    """
    Class for serializing the Post model
    """

    snippet = serializers.ReadOnlyField(source="get_snippet")
    relative_path = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "relative_path",
            "author",
            "title",
            "content",
            "snippet",
            "image",
            "category",
            "status",
            "published_date",
            "created_date",
        ]
        read_only_fields = ["author", "status", "created_date"]

    def get_categories(self, obj):
        """
        Getting Categories for each Post
        """
        post = Post.objects.get(title=obj)
        category = CategorySerializer(post.category.all(), many=True)
        return category.data

    def get_relative_path(self, obj):
        """
        Building absolute url for each post
        """
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)

    def to_representation(self, instance):
        """
        Overriding to_representation method to separate between getting a
        list of Posts or retrieving one post.
        """
        rep = super().to_representation(instance)
        request = self.context.get("request")
        rep["category"] = self.get_categories(instance)
        rep["author"] = CustomUserSerializer(
            User.objects.get(email=instance.author.user)
        ).data
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("snippet")
            rep.pop("relative_path")
            rep["comment"] = CommentSerializer(
                Comment.objects.filter(post=instance), many=True
            ).data
        else:
            rep.pop("content")
        return rep

    def create(self, validated_data):
        """
        Creating a post with author is the user that is currently
        authenticated and automatically set status to True if published_date
        field is less than or equal to now (datetime).
        """
        author = Profile.objects.get(
            user__email=self.context.get("request").user
        )
        validated_data["author"] = author
        validated_data["status"] = now() >= validated_data["published_date"]
        return super().create(validated_data)
