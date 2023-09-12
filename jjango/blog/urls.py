from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="index"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    # path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    # path('write/', views.write, name="write"),
    path('board/', views.board, name="board"),
    path("signup/", views.signup, name="signup"),

    #게시글
    path('post/create/',
          views.create_post, name='create_post'),
     path('post/modify/<int:post_id>/',
          views.modify_post, name='modify_post'),
     path('post/delete/<int:post_id>/',
          views.delete_post, name='delete_post'),   
    
    #댓글
    path('comment/create/post/<int:post_id>/', views.create_comment, name='create_comment'),
    path('comment/modify/post/<int:comment_id>/', views.modify_comment, name='modify_comment'),
    path('comment/delete/post/<int:comment_id>/', views.delete_comment, name='delete_comment'),

]
