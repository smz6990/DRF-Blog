from django.core.management.base import BaseCommand
from datetime import datetime

from blog.models import Post


class Command(BaseCommand):
    help = "Check status for every posts"

    def handle(self, *args, **options):
        posts = Post.objects.filter(
            status=False, published_date__lte=datetime.now()
        )

        if posts.count() > 0:
            change = 0
            for post in posts:
                post.status = True
                post.save()
                change += 1
            if change:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully {change} Post(s) published!"
                    )
                )
            else:
                self.stdout.write(
                    self.style.NOTICE("There is no new post to publish!")
                )
        else:
            self.stdout.write(
                self.style.NOTICE("Every post is published!")
            )
