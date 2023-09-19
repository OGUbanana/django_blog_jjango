from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet
from django.contrib.auth import views as auth_views
from .forms import CustomAuthForm
from django.conf.urls.static import static
from django.conf import settings

app_name = "blog"


router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)


urlpatterns = [
    path('', views.index, name="index"),
    path('<str:topic>', views.index, name='index_topic'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', authentication_form=CustomAuthForm), name='login'),
     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('board/', views.board, name="board"),
    #게시글
    path('write/',
          views.create_post, name='create_post'),
     path('edit_post/<int:post_id>', views.create_post, name='create_post'),

     # 토픽별 분류 - 아직 진행중(23.09.14)
    path('post_list/<str:post_topic>/', views.index, name='post_topic'),
    
    #댓글
    path('comment/create/post/<int:post_id>/', views.create_comment, name='create_comment'),
    path('comment/modify/post/<int:comment_id>/', views.modify_comment, name='modify_comment'),
    path('comment/delete/post/<int:comment_id>/', views.delete_comment, name='delete_comment'),

    path('api/', include(router.urls)),
    path('board/<int:post_id>/', views.board, name='post_detail')
    

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)