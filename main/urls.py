# main/urls.py - убедись что есть все маршруты
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='home'),
    path('main_list/', views.main_list, name='main_list'),
    path('list_users/', views.list_users, name='list_users'),
    path('register/', views.register_view, name='register'),
    path('user/<int:user_id>/', views.user_detail, name='user_detail'),
    path('user/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('user/<int:user_id>/edit/', views.edit_user, name='edit_user'),
]