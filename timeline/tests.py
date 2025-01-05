from django.test import TestCase, Client, SimpleTestCase
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from .models import Profile, Post, Comment, Like, Follow
from .forms import ProfileUpdateForm, CommentForm
from .views import timeline, follow_user, unfollow_user, search_posts, edit_post, post_detail, like_post, delete_post, edit_profile, profile_view
from accounts.views import CustomLoginView
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


class FollowModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', password='pass1')
        self.user2 = User.objects.create_user(
            username='user2', password='pass2')
        self.follow = Follow.objects.create(
            follower=self.user1, followed=self.user2)

    def test_follow_creation(self):
        self.assertTrue(isinstance(self.follow, Follow))
        self.assertEqual(self.follow.__str__(
        ), f"{self.user1.username} follows {self.user2.username}")


# Views.pyのテスト
class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.profile = Profile.objects.get_or_create(user=self.user)
        self.client.login(username='testuser', password='testpass')

    def test_profile_view(self):
        response = self.client.get(
            reverse('profile', args=[self.user.username]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'timeline/profile.html')
        self.assertContains(response, self.user.username)


class EditProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.profile, created = Profile.objects.get_or_create(user=self.user)
        self.client.login(username='testuser', password='testpass')

    def test_get_edit_profile(self):
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'timeline/edit_profile.html')

    def test_post_edit_profile(self):
        response = self.client.post(reverse('edit_profile'), {
            'bio': 'New bio',
            'location': 'New location',
        })
        self.assertRedirects(response, reverse(
            'profile', args=[self.user.username]))
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, 'New bio')
        self.assertEqual(self.profile.location, 'New location')

# タイムラインテスト


class TimelineViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.post = Post.objects.create(
            user=self.user, content='This is a test post')
        self.client.login(username='testuser', password='testpass')

    def test_timeline_view(self):
        response = self.client.get(reverse('timeline'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'timeline/timeline.html')
        self.assertContains(response, self.post.content)


# フォロー機能のテスト
class FollowUnfollowViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='user1', password='pass')
        self.user2 = User.objects.create_user(
            username='user2', password='pass')
        self.client.login(username='user1', password='pass')

    def test_follow_user(self):
        response = self.client.get(
            reverse('follow_user', args=[self.user2.id]))
        self.assertRedirects(response, reverse('timeline'))
        self.assertTrue(Follow.objects.filter(
            follower=self.user1, followed=self.user2).exists())

    def test_unfollow_user(self):
        Follow.objects.create(follower=self.user1, followed=self.user2)
        response = self.client.get(
            reverse('unfollow_user', args=[self.user2.id]))
        self.assertRedirects(response, reverse('timeline'))
        self.assertFalse(Follow.objects.filter(
            follower=self.user1, followed=self.user2).exists())


# forms.pyのテスト
class ProfileUpdateFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.profile = Profile.objects.get_or_create(user=self.user)[0]

    def test_valid_profile_update_form(self):
        form_data = {
            'bio': 'This is a test bio',
            'profile_image': 'path/to/image.jpg',
            'cover_image': 'path/to/cover.jpg',
            'location': 'Tokyo',
            'website': 'https://example.com'
        }
        form = ProfileUpdateForm(data=form_data, instance=self.profile)
        self.assertTrue(form.is_valid())
        updated_profile = form.save()
        self.assertEqual(updated_profile.bio, 'This is a test bio')
        self.assertEqual(updated_profile.location, 'Tokyo')


class CommentFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.post = Post.objects.create(
            user=self.user, content='This is a test post')

    def test_valid_comment_form(self):
        form_data = {
            'content': 'This is a test comment'
        }
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())
        comment = form.save(commit=False)
        comment.post = self.post
        comment.user = self.user
        comment.save()
        self.assertEqual(comment.content, 'This is a test comment')


# urls.pyのテスト
class TestUrls(SimpleTestCase):

    def test_timeline_url(self):
        url = reverse('timeline')
        self.assertEquals(resolve(url).func, timeline)

    def test_follow_user_url(self):
        url = reverse('follow_user', args=[1])
        self.assertEquals(resolve(url).func, follow_user)

    def test_unfollow_user_url(self):
        url = reverse('unfollow_user', args=[1])
        self.assertEquals(resolve(url).func, unfollow_user)

    def test_search_posts_url(self):
        url = reverse('search_posts')
        self.assertEquals(resolve(url).func, search_posts)

    def test_edit_post_url(self):
        url = reverse('edit_post', args=[1])
        self.assertEquals(resolve(url).func, edit_post)

    def test_post_detail_url(self):
        url = reverse('post_detail', args=[1])
        self.assertEquals(resolve(url).func, post_detail)

    def test_like_post_url(self):
        url = reverse('like_post', args=[1])
        self.assertEquals(resolve(url).func, like_post)

    def test_delete_post_url(self):
        url = reverse('delete_post', args=[1])
        self.assertEquals(resolve(url).func, delete_post)

    def test_edit_profile_url(self):
        url = reverse('edit_profile')
        self.assertEquals(resolve(url).func, edit_profile)

    def test_profile_view_url(self):
        url = reverse('profile', args=['username'])
        self.assertEquals(resolve(url).func, profile_view)

    def test_account_login_url(self):
        url = reverse('account_login')
        self.assertEquals(resolve(url).func.view_class, CustomLoginView)
