# Generated by Django 4.2.5 on 2023-09-13 07:18

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('post_id', models.AutoField(primary_key=True, serialize=False)),
                ('post_title', models.CharField(max_length=255)),
                ('post_content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='내용')),
                ('post_topic', models.CharField(max_length=10)),
                ('post_created_at', models.DateTimeField(auto_now_add=True)),
                ('post_views', models.IntegerField(default=0)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.AutoField(primary_key=True, serialize=False)),
                ('comment_writer', models.CharField(max_length=255)),
                ('comment_content', models.TextField()),
                ('comment_created_at', models.DateTimeField(auto_now_add=True)),
                ('comment_modifed_at', models.DateTimeField(auto_now_add=True)),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.post')),
            ],
        ),
    ]
