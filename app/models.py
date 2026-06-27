from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """扩展用户模型"""

    class Meta:
        db_table = 'app_user'
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.username


class Profile(models.Model):
    """用户个人信息"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='用户')
    name = models.CharField('姓名', max_length=30)
    sex = models.CharField('性别', max_length=2, choices=(('男', '男'), ('女', '女')), blank=True)
    birth = models.DateField('出生日期', null=True, blank=True)
    phone = models.CharField('电话', max_length=20)
    email = models.EmailField('邮箱', max_length=50, blank=True)
    address = models.CharField('地址', max_length=100, blank=True)

    class Meta:
        verbose_name = '个人信息'
        verbose_name_plural = '个人信息'

    def __str__(self):
        return f"{self.user.username} 的个人信息"


class Schedule(models.Model):
    """日程安排"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schedules', verbose_name='用户')
    title = models.CharField('标题', max_length=100)
    text = models.TextField('内容', max_length=500, blank=True)
    start_time = models.DateTimeField('开始时间', null=True, blank=True)
    end_time = models.DateTimeField('结束时间', null=True, blank=True)

    class Meta:
        ordering = ['-start_time']
        verbose_name = '日程'
        verbose_name_plural = '日程'

    def __str__(self):
        return self.title
