from django.test import TestCase
from django.contrib.auth import get_user_model
from app.models import Profile
from app.forms import ProfileForm, ScheduleForm

User = get_user_model()


class ProfileFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.profile = Profile.objects.create(user=self.user)

    def test_valid_data(self):
        form = ProfileForm(data={
            'name': '张三',
            'phone': '13800138000',
            'email': 'test@example.com',
        }, instance=self.profile)
        self.assertTrue(form.is_valid())

    def test_name_required(self):
        form = ProfileForm(data={'phone': '13800138000'}, instance=self.profile)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_name_too_short(self):
        form = ProfileForm(data={'name': 'A', 'phone': '13800138000'}, instance=self.profile)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_phone_required(self):
        form = ProfileForm(data={'name': '张三'}, instance=self.profile)
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)

    def test_phone_invalid_chars(self):
        form = ProfileForm(data={'name': '张三', 'phone': 'abc'}, instance=self.profile)
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)

    def test_phone_too_short(self):
        form = ProfileForm(data={'name': '张三', 'phone': '12345'}, instance=self.profile)
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)

    def test_international_phone_valid(self):
        form = ProfileForm(data={'name': '张三', 'phone': '+1 202-555-0123'}, instance=self.profile)
        self.assertTrue(form.is_valid())

    def test_china_with_country_code(self):
        form = ProfileForm(data={'name': '张三', 'phone': '+86 138 0013 8000'}, instance=self.profile)
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        form = ProfileForm(data={
            'name': '张三',
            'phone': '13800138000',
            'email': 'invalid',
        }, instance=self.profile)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_valid_email(self):
        form = ProfileForm(data={
            'name': '张三',
            'phone': '13800138000',
            'email': 'test@example.com',
        }, instance=self.profile)
        self.assertTrue(form.is_valid())

    def test_blank_email_allowed(self):
        form = ProfileForm(data={'name': '张三', 'phone': '13800138000'}, instance=self.profile)
        self.assertTrue(form.is_valid())
