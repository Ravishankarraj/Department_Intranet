from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('profile', views.profile, name='profile'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('approve', views.approve, name='approve'),
    path('delete', views.delete, name='delete'),
    path('edit', views.edit, name='edit'),
    path('postnotice', views.postnotice, name='postnotice'),
    path('loginpage', views.index, name='index'),
    path('postednotice', views.postednotice, name="postednotice"),
    path('pendingnotice', views.pendingnotice, name="pendingnotice"),
    path('leavemanagement', views.leave_management, name='leavemanagement'),
    path('new_notice', views.new_notice, name="new_notice"),
]
