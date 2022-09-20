from django.urls import path

from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.BlogIndexView.as_view(), name='index'),
    path('<int:pk>/', views.BlogSingleView.as_view(), name='single'),
    path('create-post/',views.BlogCreatePostView.as_view(), name='create-post'),
    path('<int:pk>/edit/', views.BlogEditPostView.as_view(), name='edit-post'),
    path('<int:pk>/delete/', views.BlogDeletePostView.as_view(), name='delete-post'),
    path('comment/',views.BlogCommentCreateView.as_view(), name='comment'),
    path('category/<str:cat_name>/',views.CategoryListView.as_view(),name='category'),
    path('category-create/',views.CategoryCreateView.as_view(),name='category-create'),
    path('search/',views.SearchView.as_view(),name='search'),
]
