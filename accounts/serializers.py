from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    posts_count = serializers.IntegerField(source="user.posts.count", read_only=True)

    class Meta:
        model = Profile
        fields = ("id", "username", "bio", "created_at", "posts_count")
