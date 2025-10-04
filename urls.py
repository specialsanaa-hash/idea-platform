"""
مسارات API لنظام المستخدمين والأدوار
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'users'

urlpatterns = [
    # مسارات المصادقة
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),
    path('auth/me/', views.CurrentUserView.as_view(), name='current_user'),
    path('auth/change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    
    # مسارات الأدوار
    path('roles/', views.RoleListCreateView.as_view(), name='role_list_create'),
    path('roles/<uuid:pk>/', views.RoleDetailView.as_view(), name='role_detail'),
    
    # مسارات المستخدمين
    path('', views.UserListCreateView.as_view(), name='user_list_create'),
    path('<uuid:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('stats/', views.user_stats, name='user_stats'),
    
    # مسارات الملف الشخصي
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
    
    # مسارات الجلسات
    path('sessions/', views.UserSessionsView.as_view(), name='user_sessions'),
    path('sessions/<int:session_id>/terminate/', views.terminate_session, name='terminate_session'),
]

