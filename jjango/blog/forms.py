from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import Post,Comment

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_content']
        labels = {
            'comment_content': '게시글 내용',
        }

class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")

class BlogPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_title' , 'post_content']
        widgets = {
            'post_title': forms.TextInput(attrs={'placeholder': '제목'}),
         }

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'ID'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    error_messages = {
        'invalid_login': '잘못된 아이디 또는 비밀번호입니다. 대소문자를 확인하여 주세요.',
        'inactive': '이 계정은 비활성화되었습니다. 관리자에게 문의하세요.',
    }

class CustomUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'ID'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Verify Password'}))
