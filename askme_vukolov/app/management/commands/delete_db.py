import random

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Tag


class Command(BaseCommand):
    text = "some text"

    def handle(self, *args, **options):
        # by deleting users we start waterfall, which remove everything except tags
        for u in User.objects.all():
            if u.is_superuser:
                continue
            u.delete()

        for tag in Tag.objects.all():
            tag.delete()

        self.stdout.write(
            self.style.SUCCESS(f'successfully delete it all')
        )


