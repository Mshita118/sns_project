from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, Post, Comment, Like, Follow
# models.pyのテスト


class ProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.profile, created = Profile.objects.get_or_create(user=self.user)

    def test_profile_creation(self):
        self.assertTrue(isinstance(self.profile, Profile))
        self.assertEqual(self.profile.__str__(), self.user.username)


class PostModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.post = Post.objects.create(
            user=self.user, content='This is a test post')

    def test_post_creation(self):
        self.assertTrue(isinstance(self.post, Post))
        self.assertEqual(self.post.__str__(),
                         f"{self.user.username}: {self.post.content[:20]}")


class CommentModelCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.post = Post.objects.create(
            user=self.user, content='This is a test post')
        self.comment = Comment.objects.create(
            post=self.post, user=self.user, content='This is a test comment')

    def test_comment_creation(self):
        self.assertTrue(isinstance(self.comment, Comment))
        self.assertEqual(self.comment.__str__(),
                         f"Comment by {self.user.username} on {self.post.id}")
