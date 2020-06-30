from django.db import models


# Create your models here.
class User(models.Model):
    sid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    name = models.CharField(max_length=30, null=True)
    sex = models.CharField(max_length=2, null=True, choices=(('男', '男'), ('女', '女')))
    birth = models.DateField(null=True)
    phone = models.CharField(max_length=20, null=True)
    email = models.EmailField(max_length=30, null=True)
    address = models.CharField(max_length=30, null=True)

    def to_list(self):
        return [
            ('name', (self.name if self.name is not None else '')),
            ('sex', (self.sex if self.sex is not None else '')),
            ('birth', (self.birth if self.birth is not None else '')),
            ('phone', (self.phone if self.phone is not None else '')),
            ('email', (self.email if self.email is not None else '')),
            ('address', (self.address if self.address is not None else ''))
        ]

    def __str__(self):
        return self.username


class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    text = models.TextField(max_length=500, null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
