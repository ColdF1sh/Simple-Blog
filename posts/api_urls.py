from django.urls import path

from .api_views import (
    CommentRetrieveAPIView,
    PostCommentListCreateAPIView,
    PostListCreateAPIView,
    PostRetrieveAPIView,
)


urlpatterns = [
    path("posts/", PostListCreateAPIView.as_view(), name="api_post_list_create"),
    path("posts/<int:pk>/", PostRetrieveAPIView.as_view(), name="api_post_detail"),
    path(
        "posts/<int:pk>/comments/",
        PostCommentListCreateAPIView.as_view(),
        name="api_post_comments",
    ),
    path(
        "comments/<int:pk>/",
        CommentRetrieveAPIView.as_view(),
        name="api_comment_detail",
    ),
]
