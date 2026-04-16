from django.urls import path

from .views import (
    HomeView,
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostUpdateView,
    add_comment_view,
)


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("post/new/", PostCreateView.as_view(), name="post_create"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("post/<int:pk>/edit/", PostUpdateView.as_view(), name="post_update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),
    path("post/<int:pk>/comment/", add_comment_view, name="add_comment"),
]
