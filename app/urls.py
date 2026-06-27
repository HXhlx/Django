from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user/<str:username>/', views.profile_view, name='profile'),
    path('user/<str:username>/edit/', views.profile_edit_view, name='profile_edit'),
    path('user/<str:username>/schedules/', views.schedule_list_view, name='schedule_list'),
    path('user/<str:username>/schedules/add/', views.schedule_add_view, name='schedule_add'),
    path('user/<str:username>/schedules/<int:pk>/edit/', views.schedule_edit_view, name='schedule_edit'),
]
