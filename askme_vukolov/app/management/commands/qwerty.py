from django.core.management.base import BaseCommand
from app.models import Tag


class Command(BaseCommand):
    text = "some text"

    def add_arguments(self, parser):
        parser.add_argument("ratio", nargs=1, type=int)

    def handle(self, *args, **options):
        ratio = options['ratio'][0]
        for i in range(ratio):
            tmp = Tag(name=f'tag-{i}')
            tmp.save()
        self.stdout.write(
            self.style.SUCCESS(f'add {ratio} tags')
        )


