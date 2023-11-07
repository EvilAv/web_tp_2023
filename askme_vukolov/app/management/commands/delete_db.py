from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Tag


class Command(BaseCommand):
    text = "some text"

    def handle(self, *args, **options):
        for u in User.objects.all():
            if u.is_superuser:
                continue
            u.delete()
        self.stdout.write(
            self.style.SUCCESS(f'delete it all')
        )


