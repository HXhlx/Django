from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import *


# Create your views here.
def home(request):
    return render(request, 'home.html')


def register(request):
    return render(request, 'register.html')


def register_confirm(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
    except KeyError:
        return render(request, 'register.html', {'username_error': '你正试图从非法途径访问该网址,请先注册!'})
    if password != confirmpassword:
        return render(request, 'register.html', {'password_error': "the password and the confirm password don't same"})
    try:
        User.objects.create(username=username, password=password)
    except IntegrityError:
        return render(request, 'register.html', {'username_error': 'the username already exists'})
    return HttpResponseRedirect(reverse('look', args=(username,)))


def login(request):
    return render(request, 'login.html')


def login_confirm(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError:
        return render(request, 'login.html', {'error_message': '你正试图从非法途径访问该网址,请先登录!'})
    if User.objects.filter(username=username, password=password).exists():
        return HttpResponseRedirect(reverse('look', args=(username,)))
    return render(request, 'login.html', {'error_message': 'username or password is wrong'})


def look(request, username):
    user = get_object_or_404(User, username=username)
    user_list = user.to_list()
    user_list.insert(0, ('password', user.password))
    return render(request, 'look.html', {'user': user, 'user_list': user_list})


def modify(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'modify.html', {'user': user, 'user_list': user.to_list()})


def modify_confirm(request, username):
    user = get_object_or_404(User, username=username)
    try:
        user.password = request.POST['password']
        user.name = (request.POST['name'] if request.POST['name'] != '' else None)
        user.sex = (request.POST['sex'] if request.POST['sex'] != '' else None)
        user.birth = (request.POST['birth'] if request.POST['birth'] != '' else None)
        user.phone = (request.POST['phone'] if request.POST['phone'] != '' else None)
        user.email = (request.POST['email'] if request.POST['email'] != '' else None)
        user.address = (request.POST['address'] if request.POST['address'] != '' else None)
    except KeyError:
        raise Http404('你正试图从非法途径访问该网址,请先登录!')
    user.save()
    return HttpResponseRedirect(reverse('look', args=(username,)))


def schedule(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'schedule.html', {'schedules': user.schedule_set.all(), 'username': username})


def insert(request, username):
    user = get_object_or_404(User, username=username)
    try:
        title = request.POST['title']
        content = (request.POST['content'] if request.POST['content'] != '' else None)
        start_time = (request.POST['start time'] if request.POST['start time'] != '' else None)
        end_time = (request.POST['end time'] if request.POST['end time'] != '' else None)
    except KeyError:
        return render(request, 'insert.html', {'username': username})
    user.schedule_set.create(title=title, text=content, start_time=start_time, end_time=end_time)
    return HttpResponseRedirect(reverse('schedule', args=(username,)))


def change(request, username, title):
    user = get_object_or_404(User, username=username)
    sch = user.schedule_set.get(title=title)
    try:
        if request.POST['operate'] == 'delete':
            sch.delete()
        elif request.POST['operate'] == 'save':
            sch.title = request.POST['title']
            sch.text = (request.POST['content'] if request.POST['content'] != '' else None)
            sch.start_time = (request.POST['start time'] if request.POST['start time'] != '' else None)
            sch.end_time = (request.POST['end time'] if request.POST['end time'] != '' else None)
            try:
                sch.save()
            except IntegrityError:
                return render(request, 'change.html', {'username': username, 'schedule': sch})
        return HttpResponseRedirect(reverse('schedule', args=(username,)))
    except KeyError:
        return render(request, 'change.html', {'username': username, 'schedule': sch})
