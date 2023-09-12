from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Post,User,Comment
from .forms import UserForm,CommentForm

# Create your views here.

# 메인 화면
def index(request):
    return render(request, 'index.html')

#회원가입
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'index.html', {'form': form})


def board(reqeust):
    return render(request, 'board.html')

# 로그인 처리
def login(request):
    if request.method == "POST":
        input_id = request.POST["user_id"]
        input_pwd = request.POST["user_pwd"]

        try :
            user = user.objects.get(user_id=input_id)

            if user.user_pwd == input_pwd:
                return render(request, "index.html", {"login" : "success", "user_name" : user.user_name})
            else :
                return render(request, "index.html", {"login": "pwd_fail"})
        except post.DoesNotExist :
            return render(request, "login.html", {"login":"user_fail"})
        
    else :
        return render(request, "login.html")
        
# 로그아웃 처리
def logout(request):
    logout(request)
    return render(request, "index.html", {"login": "logout"})

# 게시글 작성 처리
@login_required(login_url='blog:login')
def create_post(request):
    if request.method == "POST" and request.FILES :
        user_name = request.POST["user_name"]
        title = request.POST["title"]
        content = request.POST["content"]
        created_at = request.POST["created_at"]
        image = request.FILES["image"]

        post.objects.create(
            user_id = user_name,
            title = title,
            content = content,
            created_at = created_at,
            image = image
        )
        return redirect("index")

    return render(request, 'write.html')

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