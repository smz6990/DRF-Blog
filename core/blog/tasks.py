from celery import shared_task, Celery
from django.utils import timezone

from .models import Post


app = Celery()


@shared_task
def publish_posts_task():
    posts = Post.objects.filter(
        status=False, published_date__lte=timezone.now()
    )
    for post in posts:
        post.status = True
        post.save()
    return (
        print(f"{posts.count()} published!")
        if posts
        else print("There is no post to publish")
    )


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        60 * 60,
        publish_posts_task().s(),
        name="published posts every one hour",
    )
