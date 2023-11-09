from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    avatar = models.ImageField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100)

    def __str__(self):
        return self.nickname


class TagManager(models.Manager):
    def _count_uses(self):
        for t in self.all():
            t.uses = t.question_set.count()
            t.save()

    def popular(self):
        self._count_uses()
        return self.order_by('-uses')


class Tag(models.Model):
    name = models.CharField(max_length=100)
    uses = models.PositiveIntegerField(default=0)

    objects = TagManager()

    def __str__(self):
        return self.name


class QuestionManager(models.Manager):
    def recent(self):
        return self.order_by('-date_time')

    def best(self):
        return self.order_by('-cur_rate')

    def by_tag(self, tag_name):
        return self.filter(tags__name=tag_name)


class Question(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    text = models.TextField(max_length=2048)
    # date_time = models.DateTimeField(auto_now_add=True)
    date_time = models.DateTimeField()
    cur_rate = models.IntegerField(default=0)
    ans_count = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField(Tag)

    objects = QuestionManager()

    def __str__(self):
        return self.title


class Answer(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    parent = models.ForeignKey(Question, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    text = models.TextField(max_length=2048)
    # date_time = models.DateTimeField(auto_now_add=True)
    date_time = models.DateTimeField()
    is_correct = models.BooleanField(default=False)
    cur_rate = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.parent.ans_count = self.parent.answer_set.count()
        self.parent.save()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.parent.ans_count = self.parent.answer_set.count()
        self.parent.save()

    def __str__(self):
        return self.title


class AbstractRate(models.Model):
    class Meta:
        abstract = True

    RATE_TYPES = [
        (1, 'like'),
        (-1, 'dislike'),
    ]
    type = models.IntegerField(choices=RATE_TYPES)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # parent = models.ForeignKey(Question, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # prevent multiple rates from one user to one question
        if self.parent.rates.filter(author=self.author).exists():
            return
        super().save(*args, **kwargs)
        self.parent.cur_rate += self.type
        self.parent.save()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.parent.cur_rate -= self.type
        self.parent.save()


class RateToQuestion(AbstractRate):
    parent = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='rates')


class RateToAnswer(AbstractRate):
    parent = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='rates')
