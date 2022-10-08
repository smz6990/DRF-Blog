from random import choice, randint
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from accounts.models import User, Profile
from blog.models import Post, Category


class Command(BaseCommand):
    help = "Create new post with the given arg (default is 5)"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def add_arguments(self, parser):

        parser.add_argument(
            "-n", "--number", type=int, help="number of posts to create"
        )

    def handle(self, *args, **options):
        post_number = options["number"] or 5
        data = {"email": self.fake.email(), "password": "a/1234567"}
        user = User.objects.create_user(**data, is_verify=True)
        profile = Profile.objects.get(user=user)
        profile.first_name = self.fake.first_name()
        profile.last_name = self.fake.last_name()
        profile.description = self.fake.paragraph(nb_sentences=2)
        profile.save()

        for _ in range(post_number):
            data = {
                "author": profile,
                "title": self.fake.sentence(nb_words=10),
                "content": self.fake.paragraph(nb_sentences=10),
                "status": choice([True, False]),
                "published_date": timezone.now(),
            }
            post = Post.objects.create(**data)
            if category := self.get_random_category():
                post.category.set((category,))
                post.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully create {post_number} post(s) by {profile}'."
            )
        )

    def get_random_category(self):
        query = Category.objects.all()
        if query:
            return query[randint(0, query.count() - 1)]
        else:
            return None
