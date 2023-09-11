from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="index"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    # path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('write/', views.write, name="write"),
    path('board/', views.board, name="board"),
    path("signup/", views.signup, name="signup"),
]
