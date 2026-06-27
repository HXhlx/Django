from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Profile, Schedule


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_active', 'date_joined']
    list_filter = ['is_active', 'is_staff', 'date_joined']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'sex', 'phone', 'email']
    search_fields = ['user__username', 'name', 'phone']


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'start_time', 'end_time']
    list_filter = ['user', 'start_time']
    search_fields = ['title', 'text']
