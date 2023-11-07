from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    avatar = models.ImageField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100)


class Tag(models.Model):
    name = models.CharField(max_length=100)


class Question(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    text = models.TextField(max_length=2048)
    date_time = models.DateTimeField(auto_now_add=True)
    cur_rate = models.IntegerField(default=0)
    ans_count = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag)


class Rate(models.Model):
    RATE_TYPES = [
        ('l', 'like'),
        ('d', 'dislike'),
    ]
    type = models.CharField(max_length=1, choices=RATE_TYPES)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    parent = models.ForeignKey(Question, on_delete=models.CASCADE)


class Answer(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    parent = models.ForeignKey(Question, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    text = models.TextField(max_length=2048)
    date_time = models.DateTimeField(auto_now_add=True)
