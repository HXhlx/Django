from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('register-confirm/', register_confirm, name='register-confirm'),
    path('login/', login, name='login'),
    path('login-confirm/', login_confirm, name='login-confirm'),
    path('look/<username>', look, name='look'),
    path('modify/<username>', modify, name='modify'),
    path('modify-confirm/<username>', modify_confirm, name='modify-confirm'),
    path('schedule/<username>', schedule, name='schedule'),
    path('schedule/<username>/add', insert, name='add'),
    path('schedule/<username>/<title>', change, name='change')
]
