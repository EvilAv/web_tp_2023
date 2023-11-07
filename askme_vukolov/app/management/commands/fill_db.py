from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Tag


class Command(BaseCommand):
    text = "some text"

    def add_arguments(self, parser):
        parser.add_argument("ratio", nargs=1, type=int)

    def handle(self, *args, **options):
        ratio = options['ratio'][0]
        for i in range(ratio):
            u = User.objects.create_user(f'@user_{i}', f'mail{i}@mail.com', 'some_pass')
            self.stdout.write(str(u.id))
            u.save()
        self.stdout.write(
            self.style.SUCCESS(f'add {ratio} users')
        )


