from django.contrib import admin
from django.urls import path
from .views import RegiterView,loginView,UserView,LogoutView

urlpatterns = [
    path('register',RegiterView.as_view()),
    path('login',loginView.as_view()),
    path('user',UserView.as_view()),
    path('logout',LogoutView.as_view()),
]