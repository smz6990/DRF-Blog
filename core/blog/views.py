from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_list_or_404
from django.utils import timezone

from accounts.models import Profile
from .models import Post, Comment
from .forms import CategoryForm, PostForm, CommentForm

class BlogIndexView(generic.ListView):
    """
    Class that show all the published posts
    """
    allow_empty = True
    context_object_name = 'posts'
    paginate_by = 4
    queryset = Post.objects.filter(status=True)
    template_name='blog/blog-index.html'
    
class BlogSingleView(generic.DetailView):
    """
    Class that show detail of a Post object
    """
    context_object_name = 'post'
    # model = Post
    queryset = Post.objects.filter(status=True)
    template_name = 'blog/blog-single.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        if obj:
            try:
                comments = Comment.objects.filter(post=obj)
            except Comment.DoesNotExist:
                pass
            else:
                data = []
                for comment in comments:
                    data.append((comment, Profile.objects.get(user__email=comment.email).image))
                context['data'] = data
        return context
    
class BlogCreatePostView(LoginRequiredMixin, generic.CreateView):
    """
    Class to create a new Post in blog app by logged in user
    """
    form_class = PostForm
    template_name = 'blog/blog-create-post.html'
    
    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.error(self.request, "Something went wrong.")
        messages.error(self.request, form.errors)
        return super().form_invalid(form)
    
    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        user = Profile.objects.get(user__email=self.request.user)
        form.instance.author = user
        if form.instance.published_date <= timezone.now():
            form.instance.status = True
        else:
            self.success_url = reverse('blog:index')
        messages.success(self.request, 'Your Post created successfully.')
        return super().form_valid(form)
    
class BlogEditPostView(LoginRequiredMixin, generic.UpdateView):
    """
    Class to update the existing post by the creator of post
    """
    form_class = PostForm
    model = Post
    template_name = 'blog/blog-update-post.html'
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = Profile.objects.get(user__email=request.user)
        if self.object.author != user:
            messages.error(request, "You can not update this post, \
                Every post only can updated by its owner")
            return HttpResponseRedirect(reverse('blog:index'))
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = Profile.objects.get(user__email=request.user)
        if self.object.author != user:
            messages.error(request, "You can not update this post, \
                Every post only can updated by its owner")
            return HttpResponseRedirect(reverse('blog:index'))
        return super().post(request, *args, **kwargs)
    
    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.error(self.request, "Something went wrong.")
        messages.error(self.request, form.errors)
        return super().form_invalid(form)
    
    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        messages.success(self.request, 'Your Post updated successfully.')
        return super().form_valid(form)
    
class BlogDeletePostView(LoginRequiredMixin, generic.DeleteView):
    """
    Class to delete an existing post by its owner
    """
    model = Post
    success_url = reverse_lazy('blog:index')
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = Profile.objects.get(user__email=request.user)
        if self.object.author != user:
            messages.error(request, "You can not delete this post, \
                Every post only can be deleted by its owner")
            return HttpResponseRedirect(reverse('blog:index'))
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = Profile.objects.get(user__email=request.user)
        if self.object.author != user:
            messages.error(request, "You can not delete this post, \
                Every post only can be deleted by its owner")
            return HttpResponseRedirect(reverse('blog:index'))
        messages.success(request, "Post deleted successfully")
        return super().post(request, *args, **kwargs)
    
    
class BlogCommentCreateView(LoginRequiredMixin, generic.CreateView):
    """
    Class to create a Comment for a post
    """
    http_method_names = ['post']
    form_class = CommentForm
    model = Comment
    template_name = 'blank.html'
    
    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.error(self.request, "Something went wrong.")
        messages.error(self.request, form.errors)
        return super().form_invalid(form)
    
    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        messages.success(self.request, 'Your Comment submit successfully.')
        return super().form_valid(form)
    
class CategoryListView(generic.ListView):
    """
    Class that show all the published posts
    """
    allow_empty = True
    context_object_name = 'posts'
    paginate_by = 4
    pk_url_kwarg = 'cat_name'
    template_name = 'blog/blog-index.html'
    
    def get_queryset(self):
        posts = Post.objects.filter(status=True, category__name=self.kwargs['cat_name'])
        return posts

class CategoryCreateView(LoginRequiredMixin, generic.CreateView):
    """
    Class to create a new Category
    """
    form_class = CategoryForm
    template_name = 'blog/category-create.html'
    success_url = reverse_lazy('blog:index')
    
    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.error(self.request, "Something went wrong.")
        messages.error(self.request, form.errors)
        return super().form_invalid(form)
    
    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        messages.success(self.request, 'New Category created successfully.')
        return super().form_valid(form)
    
class SearchView(generic.ListView):
    """
    Class to search based on content field in Post model.
    """
    allow_empty = True
    context_object_name = 'posts'
    paginate_by = 4
    template_name = 'blog/blog-index.html'
    
    def get_queryset(self):
        posts = Post.objects.filter(status=True, content__contains=self.request.GET['Search'])
        return posts