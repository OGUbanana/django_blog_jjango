from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .models import post, user


# Create your views here.

# 메인 화면
def index(request):
    return render(request, 'index.html')

def signup(request) :
   pass

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
def write(request):
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

def board(request):
    return render(request, 'board.html')