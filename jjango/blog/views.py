from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import openai
import html
import re
from django.http import HttpResponseNotFound
from django.conf import settings
from .models import Post,Comment, Images
from rest_framework.decorators import action
from rest_framework.response import Response
from .forms import CommentForm, BlogPost, CustomAuthForm
from rest_framework import viewsets
from .serializers import PostSerializer, CommentSerializer
from django.db.models import Max
from .parsing_image import get_images

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    @action(detail=False)
    def unpublished(self, request):
        queryset = self.queryset.filter(post_publish='N')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


# Create your views here.
def index(request, post_topic=None):
    if post_topic:
        posts = Post.objects.filter(post_topic=post_topic, post_publish='Y').order_by('-post_views')

    else:
        posts = Post.objects.filter(post_publish='Y').order_by('-post_views') 
    context = {'posts': posts}
    return render(request, 'index.html', context)

# def topic_post(request, topic=None) :
#     if topic:
#         posts = Post.objects.filter(post_topic=topic, post_publish='Y').order_by('-post_views')

#         most_viewed = Post.objects.filter(post_topic=topic, post_publish='Y').aggregate(most_view = Max('post_views'))
#         print(most_viewed)
#         most_viewed_post = list(Post.objects.filter(post_views=most_viewed['most_view']))
#         print(most_viewed_post[0])
        
#     context = {'latest_post': most_viewed_post[0], 'posts': posts}
#     return render(request, 'index_topic.html', {'posts':posts})

# 특정 주제로 필터링 
# def post_list(request, post_topic=None):

#     if post_topic:
#         posts = Post.objects.filter(post_topic=post_topic, post_publish='Y').order_by('-post_views')

#     else:
#         posts = Post.objects.filter(post_publish='Y').order_by('-post_views') 
#     return render(request, 'post_list.html', {'posts': posts})



def board(request,post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == 'POST': 
        if 'delete-button' in request.POST:
            post.delete()
            messages.success(request, "게시글이 삭제되었습니다.")
            return redirect('blog:index')
        
    post.post_views += 1
    post.save()
    sub_posts = Post.objects.filter(post_topic=post.post_topic, post_publish='Y').exclude(post_id=post.post_id).order_by('-post_created_at')[:2]
    previous_post = Post.objects.filter(post_id__lt=post.post_id, post_publish='Y').order_by('-post_id').first()
    next_post = Post.objects.filter(post_id__gt=post.post_id, post_publish='Y').order_by('post_id').first()
    context = {
        'post': post,
        'sub_posts': sub_posts,
        'previous_post': previous_post,
        'next_post': next_post,
        }
    
    return render(request, 'board.html', context)
  
def login(request):
    if request.user.is_authenticated:
        return redirect('blog:index')
    else:
        form = CustomAuthForm(data=request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('blog:index')
        return render(request, 'login.html', {'form': form})

# 로그아웃 처리
def logout(request):
    logout(request)
    return render(request, "index.html", {"login": "logout"})

def autocomplete(post_title):
    api_key = settings.OPENAI_API_KEY
                
    response_generator = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": f"당신은 '{post_title}'에 대한 블로그 포스트를 작성에 도움을 주는 비서입니다."},
            {"role": "user", "content": f"'{post_title}'에 대한 블로그 글을 작성해주세요. 제목은 제외하고 블로그 글만 써주세요. 200자 이내로만 작성하고 문장은 완성형."},
        ],
        stream=True,
        max_tokens=400,
        n=1,
        api_key=api_key  
    )   
    return response_generator




# 게시글 작성 처리

@login_required(login_url='blog:login')
def create_post(request, post_id=None):
    temporary_cnt=Post.objects.filter(post_publish='N').count()
    post = None
    if post_id:
       post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        form = BlogPost(request.POST)
        if form.is_valid():
            content= request.POST.get("post_content")
            contents=html.unescape(content)
            publish_status = request.POST.get("temporary-button", "Y")
            images = get_images(contents)
            if request.FILES:
                img = request.FILES['post_image']
            elif not request.FILES and images:
                img = images[0]
            else:
                img = '/media/basic/django.jpg'
                
            new_post = Post()  # 새로운 Post 객체 생성
            new_post.user_id=request.user
            new_post.post_title=request.POST.get("post_title")
            new_post.post_content=contents
            new_post.post_topic=request.POST.get("post_topic")
            new_post.post_image=img
            new_post.post_publish=publish_status

            
             # 새로운 Post 객체의 속성 설정 후 save() 호출
            new_post.save()
            
             
            if request.FILES:
                 for image in request.FILES.values():
                     Images.objects.create(
                         post_id=new_post,
                         image=image
                     )
            if images:
                 for image in images[1:]:
                     Images.objects.create(
                         post_id=new_post,
                         image=image
                     )

            return redirect('blog:post_detail', post_id=new_post.post_id)

    else:  # GET 요청인 경우
        initial_data={}
        if(post):
            initial_data={
              'post_title':post.post_title,
              'post_content':post.post_content,
              'post_topic':post.post_topic
              }
        form = BlogPost(initial=initial_data)

    return render(request, 'write.html', {'post': post, 'form': form, 'edit_mode': post_id is not None,'temporary_cnt':temporary_cnt})






#댓글 등록
@login_required(login_url='blog:login')
def create_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.comment_writer = request.user
            comment.comment_created_at = timezone.now()
            comment.post_id = post.id
            comment.save()
            return redirect('blog:board', post_id=post.id)
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'board.html', context)

#댓글 수정
@login_required(login_url='blog:login')
def modify_comment(request, comment_id):

    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.comment_writer:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('index', post_id=comment.post_id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('index', post_id=comment.post_id)
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'board.html', context)

#댓글 삭제
@login_required(login_url='blog:login')
def delete_comment(request, comment_id):
    
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.comment_writer:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('index', post_id=comment.post_id)
    else:
        comment.delete()
    return redirect('board', post_id=comment.post_id)

