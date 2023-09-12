from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_pwd = models.CharField(max_length=255)
    user_authority = models.CharField(max_length=100)
    user_name = models.CharField(max_length=255)

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='post_images/')
    
class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    writer = models.CharField(max_length=255)

