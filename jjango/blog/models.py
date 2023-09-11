from django.db import models

# Create your models here.
class Post(models.Model):
    id = models.AutoField(primary_key=True),models.IntegerField(max_length=11)
    user_id = models.ForeignKey(on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=1000)
    created_at = models.DateField(auto_now_add=True)
    image = models.ImageField()
    
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_pwd = models.CharField(max_length=20)
    user_authority = models.fields()
    user_name = models.CharField(10)
    
class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True,unique=True)
    post_id = models.AutoField(Post, on_delete=models.CASCADE)
    writer = models.CharField(max_length=10)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)