from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Comment, Post


User = get_user_model()


class PostModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="author",
            email="author@example.com",
            password="StrongPass123",
        )
        self.post = Post.objects.create(
            title="Model Test Post",
            content="Model test content.",
            author=self.user,
        )

    def test_post_string_representation(self):
        self.assertEqual(str(self.post), "Model Test Post")

    def test_post_absolute_url(self):
        self.assertEqual(
            self.post.get_absolute_url(),
            reverse("post_detail", kwargs={"pk": self.post.pk}),
        )


class CommentModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="commenter",
            email="commenter@example.com",
            password="StrongPass123",
        )
        self.post = Post.objects.create(
            title="Post With Comment",
            content="Content",
            author=self.user,
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content="Nice article!",
        )

    def test_comment_string_representation(self):
        expected = f"Comment by {self.user.username} on {self.post.title}"
        self.assertEqual(str(self.comment), expected)


class PostViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="writer",
            email="writer@example.com",
            password="StrongPass123",
        )
        self.other_user = User.objects.create_user(
            username="reader",
            email="reader@example.com",
            password="StrongPass123",
        )
        self.post = Post.objects.create(
            title="Testing Post",
            content="Testing post content.",
            author=self.user,
        )

    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Testing Post")

    def test_post_detail_page_loads(self):
        response = self.client.get(reverse("post_detail", kwargs={"pk": self.post.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Testing post content.")

    def test_authenticated_user_can_create_post(self):
        self.client.login(username="writer", password="StrongPass123")

        response = self.client.post(
            reverse("post_create"),
            {"title": "Created in test", "content": "New post content"},
        )

        created_post = Post.objects.get(title="Created in test")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("post_detail", kwargs={"pk": created_post.pk}))
        self.assertEqual(created_post.author, self.user)

    def test_unauthenticated_user_cannot_create_post(self):
        response = self.client.post(
            reverse("post_create"),
            {"title": "Blocked Post", "content": "Should not be created"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)
        self.assertFalse(Post.objects.filter(title="Blocked Post").exists())

    def test_protected_post_edit_requires_author(self):
        self.client.login(username="reader", password="StrongPass123")

        response = self.client.get(reverse("post_update", kwargs={"pk": self.post.pk}))

        self.assertEqual(response.status_code, 403)

    def test_authenticated_user_can_add_comment(self):
        self.client.login(username="reader", password="StrongPass123")

        response = self.client.post(
            reverse("add_comment", kwargs={"pk": self.post.pk}),
            {"content": "This comment was added in a test."},
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("post_detail", kwargs={"pk": self.post.pk}))
        self.assertTrue(
            Comment.objects.filter(
                post=self.post,
                author=self.other_user,
                content="This comment was added in a test.",
            ).exists()
        )

    def test_unauthenticated_user_cannot_add_comment(self):
        response = self.client.post(
            reverse("add_comment", kwargs={"pk": self.post.pk}),
            {"content": "Anonymous comment"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)
        self.assertFalse(Comment.objects.filter(content="Anonymous comment").exists())
