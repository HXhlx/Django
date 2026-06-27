from django.test import TestCase
from django.contrib.auth import get_user_model
from app.models import Profile, Schedule
import datetime

User = get_user_model()


class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.profile = Profile.objects.create(user=self.user, name='测试用户', phone='13800138000')

    def test_profile_creation(self):
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(str(profile), 'testuser 的个人信息')

    def test_profile_fields(self):
        self.profile.name = '测试用户2'
        self.profile.phone = '13900139000'
        self.profile.save()
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.name, '测试用户2')
        self.assertEqual(self.profile.phone, '13900139000')

    def test_schedule_creation(self):
        schedule = Schedule.objects.create(
            user=self.user,
            title='测试日程',
            text='测试内容',
            start_time=datetime.datetime.now(),
        )
        self.assertEqual(str(schedule), '测试日程')

    def test_schedule_ordering(self):
        now = datetime.datetime.now()
        later = now + datetime.timedelta(hours=1)
        schedule1 = Schedule.objects.create(user=self.user, title='日程1', start_time=now)
        schedule2 = Schedule.objects.create(user=self.user, title='日程2', start_time=later)
        schedules = Schedule.objects.all()
        self.assertEqual(schedules[0], schedule2)
        self.assertEqual(schedules[1], schedule1)
