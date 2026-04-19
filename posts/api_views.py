from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions

from .models import Comment, Post
from .serializers import CommentSerializer, PostSerializer


class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.select_related("author").all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.select_related("author").all()
    serializer_class = PostSerializer


class PostCommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.select_related("author", "post").filter(
            post_id=self.kwargs["pk"]
        )

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs["pk"])
        serializer.save(author=self.request.user, post=post)


class CommentRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Comment.objects.select_related("author", "post").all()
    serializer_class = CommentSerializer
