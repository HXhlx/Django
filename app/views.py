from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _

from .models import User, Profile, Schedule
from .forms import RegisterForm, ProfileForm, ScheduleForm


def home(request):
    return render(request, 'app/home.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, _('注册成功！'))
            return redirect('profile', username=user.username)
    else:
        form = RegisterForm()
    return render(request, 'app/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, _('登录成功！'))
            return redirect('profile', username=user.username)
        else:
            messages.error(request, _('用户名或密码错误'))
    return render(request, 'app/login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, _('已退出登录'))
    return redirect('home')


@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    if request.user != user:
        messages.error(request, _('无权访问他人个人信息'))
        return redirect('home')
    profile, _created = Profile.objects.get_or_create(user=user)
    return render(request, 'app/profile.html', {'profile_user': user, 'profile': profile})


@login_required
def profile_edit_view(request, username):
    user = get_object_or_404(User, username=username)
    if request.user != user:
        messages.error(request, _('无权修改他人个人信息'))
        return redirect('home')
    profile, _created = Profile.objects.get_or_create(user=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, _('个人信息修改成功！'))
            return redirect('profile', username=username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'app/profile_edit.html', {'form': form, 'profile_user': user})


@login_required
def schedule_list_view(request, username):
    user = get_object_or_404(User, username=username)
    if request.user != user:
        messages.error(request, _('无权查看他人日程'))
        return redirect('home')

    schedules = Schedule.objects.filter(user=user)

    search_query = request.GET.get('q', '')
    if search_query:
        schedules = schedules.filter(title__icontains=search_query)

    paginator = Paginator(schedules, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'app/schedule.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'user': user,
    })


@login_required
def schedule_add_view(request, username):
    user = get_object_or_404(User, username=username)
    if request.user != user:
        messages.error(request, _('无权为他人添加日程'))
        return redirect('home')

    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.user = user
            schedule.save()
            messages.success(request, _('日程添加成功！'))
            return redirect('schedule_list', username=username)
    else:
        form = ScheduleForm()
    return render(request, 'app/schedule_add.html', {'form': form, 'user': user})


@login_required
def schedule_edit_view(request, username, pk):
    user = get_object_or_404(User, username=username)
    if request.user != user:
        messages.error(request, _('无权修改他人日程'))
        return redirect('home')

    schedule = get_object_or_404(Schedule, pk=pk, user=user)

    if request.method == 'POST':
        if request.POST.get('operate') == 'delete':
            schedule.delete()
            messages.success(request, _('日程已删除'))
            return redirect('schedule_list', username=username)

        form = ScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            messages.success(request, _('日程修改成功！'))
            return redirect('schedule_list', username=username)
    else:
        form = ScheduleForm(instance=schedule)
    return render(request, 'app/schedule_edit.html', {'form': form, 'schedule': schedule, 'user': user})
