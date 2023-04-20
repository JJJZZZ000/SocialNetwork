from django.db import models
from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from urllib.parse import urlencode

from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response

class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    followings = models.ManyToManyField(User, related_name='followings')


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    content = models.CharField(max_length=10000)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'id={self.id}, content="{self.content}"'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    content = models.CharField(max_length=10000)
    date = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'id={self.id}, content="{self.content}"'


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    bio = models.CharField(max_length=10000, blank=True)
    profile_picture = models.FileField(blank=True)
    content_type = models.CharField(max_length=50, default='jpg')

    def __str__(self):
        return f'id={self.id}, content="{self.bio}"'
