from django import template

from blog.models import Post

register = template.Library()


@register.inclusion_tag("website/index-latest-posts.html")
def website_latest_posts():
    posts = Post.objects.filter(status=True)
    count = posts.count()
    if count < 6:
        return {"posts": posts}
    else:
        return {"posts": posts[:6]}


@register.inclusion_tag("website/index-popular-posts.html")
def website_popular_posts():
    posts = Post.objects.filter(status=True)
    count = posts.count()
    if count < 4:
        return {"posts": posts}
    else:
        return {"posts": posts[:4]}
