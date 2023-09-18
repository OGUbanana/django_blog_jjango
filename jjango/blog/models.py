from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=255)
    post_content = RichTextUploadingField('내용', blank=True, null=True)
    post_topic = models.CharField(max_length=10)
    post_publish = models.CharField(max_length=1, default='Y')
    post_created_at = models.DateTimeField(auto_now_add=True)
    post_views = models.IntegerField(default=0)
    post_image = models.ImageField(null=True, upload_to="", blank=True)



class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_writer = models.CharField(max_length=255)
    comment_content = models.TextField()
    comment_created_at = models.DateTimeField(auto_now_add=True)
    comment_modifed_at = models.DateTimeField(auto_now_add=True)
