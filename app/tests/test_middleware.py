from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings


class I18nMiddlewareTest(TestCase):
    def test_language_cookie_set(self):
        client = Client()
        response = client.get(reverse('home') + '?lang=en')
        self.assertEqual(response.status_code, 200)
        self.assertIn('django_language', response.cookies)
        self.assertEqual(response.cookies['django_language'].value, 'en')

    def test_language_switch_to_chinese(self):
        client = Client()
        response = client.get(reverse('home') + '?lang=zh-hans')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.cookies['django_language'].value, 'zh-hans')

    def test_invalid_language_ignored(self):
        client = Client()
        response = client.get(reverse('home') + '?lang=invalid')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('django_language', response.cookies)

    def test_default_language(self):
        client = Client()
        response = client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(settings.LANGUAGE_CODE, 'zh-hans')

    def test_language_persists(self):
        client = Client()
        response = client.get(reverse('home') + '?lang=en')
        self.assertEqual(response.cookies['django_language'].value, 'en')
        response2 = client.get(reverse('home'))
        self.assertEqual(response2.status_code, 200)
