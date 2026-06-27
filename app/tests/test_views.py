from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from app.models import Profile

User = get_user_model()


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.profile1 = Profile.objects.create(user=self.user1, name='用户1', phone='13800138000')
        self.profile2 = Profile.objects.create(user=self.user2, name='用户2', phone='13800138000')

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_profile_view_own(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('profile', args=['user1']))
        self.assertEqual(response.status_code, 200)

    def test_profile_view_other_forbidden(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('profile', args=['user2']))
        self.assertRedirects(response, reverse('home'))

    def test_profile_edit_own(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('profile_edit', args=['user1']))
        self.assertEqual(response.status_code, 200)

    def test_profile_edit_other_forbidden(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('profile_edit', args=['user2']))
        self.assertRedirects(response, reverse('home'))

    def test_profile_edit_post(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.post(reverse('profile_edit', args=['user1']), {
            'name': '张三',
            'phone': '13800138000',
        })
        self.assertRedirects(response, reverse('profile', args=['user1']))
        self.profile1.refresh_from_db()
        self.assertEqual(self.profile1.name, '张三')

    def test_schedule_list_own(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('schedule_list', args=['user1']))
        self.assertEqual(response.status_code, 200)

    def test_schedule_list_other_forbidden(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('schedule_list', args=['user2']))
        self.assertRedirects(response, reverse('home'))

    def test_schedule_add_own(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('schedule_add', args=['user1']))
        self.assertEqual(response.status_code, 200)

    def test_schedule_add_other_forbidden(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('schedule_add', args=['user2']))
        self.assertRedirects(response, reverse('home'))

    def test_login_success(self):
        response = self.client.post(reverse('login'), {
            'username': 'user1',
            'password': 'pass123',
        })
        self.assertRedirects(response, reverse('profile', args=['user1']))

    def test_login_failure(self):
        response = self.client.post(reverse('login'), {
            'username': 'user1',
            'password': 'wrongpass',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_logout(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('home'))
