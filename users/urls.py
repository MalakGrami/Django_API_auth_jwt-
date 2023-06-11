from django.contrib import admin
from django.urls import path
from .views import RegiterView,loginView,UserAPIView,LogoutAPIView,RefreshAPIView

urlpatterns = [
    path('register',RegiterView.as_view()),
    path('login',loginView.as_view()),
    path('user',UserAPIView.as_view()),
    path('refreshToken',RefreshAPIView.as_view()),
    path('logout',LogoutAPIView.as_view()),
]