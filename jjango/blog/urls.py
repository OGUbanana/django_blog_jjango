from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PostViewSet, CommentViewSet
from django.contrib.auth import views as auth_views
from .forms import CustomAuthForm

app_name = "blog"


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)


urlpatterns = [
    path('', views.index, name="index"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', authentication_form=CustomAuthForm), name='login'),
    # path('login/', views.login, name="login"),
     #path('logout/', views.logout, name="logout"),
     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
#     path('write/', views.write, name="write"),
    path('board/', views.board, name="board"),
    path("signup/", views.signup, name="signup"),

    #게시글
    path('write/',
          views.create_post, name='create_post'),
     path('post/modify/<int:post_id>/',
          views.modify_post, name='modify_post'),
     path('post/delete/<int:post_id>/',
          views.delete_post, name='delete_post'),   
    
    #댓글
    path('comment/create/post/<int:post_id>/', views.create_comment, name='create_comment'),
    path('comment/modify/post/<int:comment_id>/', views.modify_comment, name='modify_comment'),
    path('comment/delete/post/<int:comment_id>/', views.delete_comment, name='delete_comment'),

    path('api/', include(router.urls)),
    path('board/<int:post_id>/', views.board, name='post_detail')

]
