from django import forms
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