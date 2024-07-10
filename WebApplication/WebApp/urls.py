
from django.urls import  path
from . import views
from .views import LoginUserView, HomeView

urlpatterns = [
    path('', views.signup, name='signup'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('home/', HomeView.as_view(), name='home'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('manage_user/<int:user_id>/', views.manage_user, name='manage_user'),
]