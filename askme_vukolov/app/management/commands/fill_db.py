from datetime import datetime

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Tag, Profile, Question, Answer, RateToAnswer, RateToQuestion
from random import randint, sample, choice
from django.utils import timezone


class Command(BaseCommand):
    text = "some text"

    def add_arguments(self, parser):
        parser.add_argument("ratio", nargs=1, type=int)

    def create_tags(self, ratio=5):
        for i in range(ratio):
            tag = Tag(name=f'tag-{i}')
            tag.save()

    def create_profiles(self, ratio):
        for i in range(ratio):
            u = User.objects.create_user(f'@user_{i}', f'mail{i}@mail.com', 'some_pass')
            u.save()
            p = Profile(user=u, nickname=f'Human #{i}')
            p.save()

    def create_questions(self, ratio, count):
        for i in range(ratio):
            author = Profile.objects.all()[i]
            text = 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Corrupti incidunt fuga dicta eaque, ' \
                   'quae impedit! '
            a_text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec sit.'
            for j in range(count):
                month = randint(1, 12)
                day = randint(1, 20)
                hour = randint(0, 23)
                minute = randint(0, 59)
                tag_idx = sample(range(Tag.objects.count()), 3)
                q = Question(author=author, title=f'Question #{i * count + j}', text=text,
                             date_time=datetime(2017, month, day, hour, minute))
                q.save()
                for idx in tag_idx:
                    tag = Tag.objects.all()[idx]
                    q.tags.add(tag)
                q.save()

                for k in range(count):
                    a_idx = randint(0, Profile.objects.count() - 1)
                    a_author = Profile.objects.all()[a_idx]
                    month = randint(1, 12)
                    day = randint(1, 20)
                    hour = randint(0, 23)
                    minute = randint(0, 59)
                    is_correct = randint(0, 10) == 0
                    a = Answer(author=a_author, parent=q, title=f'Answer #{i * count * count + j * count + k}',
                               text=a_text, date_time=datetime(2018, month, day, hour, minute), is_correct=is_correct)
                    a.save()

    def create_rates(self, ratio, count):
        for i in range(ratio):
            author = Profile.objects.all()[i]
            q_idxs = sample(range(Question.objects.count()), count)
            for idx in q_idxs:
                q = Question.objects.all()[idx]
                tmp = choice(RateToQuestion.RATE_TYPES)
                r = RateToQuestion(author=author, parent=q, type=tmp[0])
                r.save()

            a_idxs = sample(range(Answer.objects.count()), count)
            for idx in a_idxs:
                q = Answer.objects.all()[idx]
                tmp = choice(RateToAnswer.RATE_TYPES)
                r = RateToAnswer(author=author, parent=q, type=tmp[0])
                r.save()

    def handle(self, *args, **options):
        ratio = options['ratio'][0]
        self.create_tags(ratio)
        self.create_profiles(ratio)
        self.create_questions(ratio, 10)
        self.create_rates(ratio, 100)
        # change label
        self.stdout.write(
            self.style.SUCCESS(
                f'add {ratio} users\nadd {ratio * 10} answers and 10 answers to each of them\nadd {ratio * 200} rates '
                f'to questions or answers\nadd {ratio} tags')
        )
