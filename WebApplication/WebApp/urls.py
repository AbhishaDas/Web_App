#app urls.py
from django.urls import  path
from . import views

urlpatterns = [
    path('', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout, name='logout'),
    path('home/', views.home, name='home'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_home/', views.admin_home, name='admin_home'),
]