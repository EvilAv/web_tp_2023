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
        (1, 'like'),
        (-1, 'dislike'),
    ]
    type = models.IntegerField(choices=RATE_TYPES)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    parent = models.ForeignKey(Question, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # prevent multiple rates from one user to one question
        if self.parent.rate_set.filter(author=self.author).exists():
            return
        super().save(*args, **kwargs)
        self.parent.cur_rate += self.type
        self.parent.save()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.parent.cur_rate -= self.type
        self.parent.save()


class Answer(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    parent = models.ForeignKey(Question, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    text = models.TextField(max_length=2048)
    date_time = models.DateTimeField(auto_now_add=True)

    # dp this in case someone very smart somehow break the data
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.parent.ans_count += 1
        self.parent.save()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.parent.ans_count -= 1
        self.parent.save()

