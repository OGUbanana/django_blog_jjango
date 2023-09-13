from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import openai
from django.conf import settings
from django.http import JsonResponse
from .models import Post,User,Comment
from .forms import CommentForm, BlogPost, CustomUserForm, CustomAuthForm
from rest_framework import viewsets
from .serializers import PostSerializer, UserSerializer, CommentSerializer

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer




# 메인 화면
def index(request):
    return render(request, 'index.html')

#회원가입
def signup(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('index')
    else:
        form = CustomUserForm()
    return render(request, 'signup.html', {'form': form})


def board(request):
    return render(request, 'board.html')

# 로그인 처리
# def login(request):
#     if request.method == "POST":
#         input_id = request.POST["user_id"]
#         input_pwd = request.POST["user_pwd"]

#         try :
#             user = user.objects.get(user_id=input_id)

#             if user.user_pwd == input_pwd:
#                 return render(request, "index.html", {"login" : "success", "user_name" : user.user_name})
#             else :
#                 return render(request, "index.html", {"login": "pwd_fail"})
#         except Post.DoesNotExist :
#             return render(request, "login.html", {"login":"user_fail"})
        
#     else :
#         return render(request, "login.html")
    
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
                    return redirect('blog:index')  # 슈퍼유저와 일반 사용자 모두 동일한 페이지로 리다이렉션
        return render(request, 'login.html', {'form': form})




        
# 로그아웃 처리
def logout(request):
    logout(request)
    return render(request, "index.html", {"login": "logout"})

# 게시글 작성 처리
@login_required(login_url='blog:login')
def create_post(request):
    # if request.method == "POST" and request.FILES :
    #     user_name = request.POST["user_name"]
    #     title = request.POST["title"]
    #     content = request.POST["content"]
    #     created_at = request.POST["created_at"]
    #     image = request.FILES["image"]
    if request.method == "POST":
        form = BlogPost(request.POST)
        
        # 폼 유효성 검사
        if form.is_valid():
            # user_name = form.cleaned_data.get("user_name", "")
            post_title = form.cleaned_data.get("post_title", "")
            content = form.cleaned_data.get("content", "")
            # created_at = form.cleaned_data.get("created_at", "")

            # GPT-3.5-turbo API 호출 및 자동완성 결과 생성
            api_key = settings.OPENAI_API_KEY
            
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[
                    {"role": "system", "content": f"당신은 '{post_title}'에 대한 블로그 포스트를 작성하는 도움이 되는 비서입니다."},
                    {"role": "user", "content": f"'{post_title}'에 대한 블로그 글을 작성해주세요. 제목은 제외하고 블로그 글만 써주세요."},
                ],
                max_tokens=400,
                n=1,
                api_key=api_key  
            )
            
            completion_text = response['choices'][0]['message']['content'].strip()
            
            last_period_index = completion_text.rfind('.')
            
            if last_period_index != -1:
               completion_text = completion_text[:last_period_index+1]
            
           # 데이터베이스에 저장
            # user, _created  = User.objects.get_or_create(user_name=user_name)
            # Post.objects.create(
            #    user_id=user.id,
            #    title=title,
            #    content=completion_text,  # AI가 생성한 내용을 content로 사용
            #    created_at=created_at
        #    )

            return JsonResponse({'completion': completion_text})

    else:  # GET 요청인 경우
        form = BlogPost()

    return render(request, 'write.html', {'form': form})

#게시글 수정
@login_required(login_url='blog:login')
def modify_post(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        
        new_title = request.POST["new_title"]
        new_content = request.POST["new_content"]

        post.title = new_title
        post.content = new_content
        post.save()

        return redirect("index")

    post_update = get_object_or_404(Post, pk=post_id)
    return render(request, 'write.html', {'post': post_update})

#게시글 삭제
@login_required(login_url='blog:login')
def delete_post(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        post.delete()
        messages.success(request, "게시글이 삭제되었습니다.")
        return redirect("index")
    
    post_delete = get_object_or_404(Post, pk=post_id)
    return render(request, 'index.html', {'post': post_delete})

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



