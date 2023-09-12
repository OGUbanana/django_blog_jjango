from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_pwd = models.CharField(max_length=255)
    user_name = models.CharField(max_length=10)
    user_authority = models.BooleanField(default=False)

class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=255)
    # post_content = models.TextField()
    post_content = RichTextUploadingField('내용', blank=True, null=True)
    post_topic = models.CharField(max_length=10)
    post_created_at = models.DateTimeField(auto_now_add=True)
    post_views = models.IntegerField(default=0)
    # post_image = models.ImageField(upload_to="static/imgs")


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_writer = models.CharField(max_length=255)
    comment_content = models.TextField()
    comment_created_at = models.DateTimeField(auto_now_add=True)
    comment_modifed_at = models.DateTimeField(auto_now_add=True)