from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """扩展用户模型"""

    class Meta:
        db_table = 'app_user'
        verbose_name = _('用户')
        verbose_name_plural = _('用户')

    def __str__(self):
        return self.username


class Profile(models.Model):
    """用户个人信息"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name=_('用户'))
    name = models.CharField(_('姓名'), max_length=30)
    sex = models.CharField(_('性别'), max_length=2, choices=(('男', _('男')), ('女', _('女'))), blank=True)
    birth = models.DateField(_('出生日期'), null=True, blank=True)
    phone = models.CharField(_('电话'), max_length=20)
    email = models.EmailField(_('邮箱'), max_length=50, blank=True)
    address = models.CharField(_('地址'), max_length=100, blank=True)

    class Meta:
        verbose_name = _('个人信息')
        verbose_name_plural = _('个人信息')

    def __str__(self):
        return _('%(username)s 的个人信息') % {'username': self.user.username}


class Schedule(models.Model):
    """日程安排"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schedules', verbose_name=_('用户'))
    title = models.CharField(_('标题'), max_length=100)
    text = models.TextField(_('内容'), max_length=500, blank=True)
    start_time = models.DateTimeField(_('开始时间'), null=True, blank=True)
    end_time = models.DateTimeField(_('结束时间'), null=True, blank=True)

    class Meta:
        ordering = ['-start_time']
        verbose_name = _('日程')
        verbose_name_plural = _('日程')

    def __str__(self):
        return self.title
