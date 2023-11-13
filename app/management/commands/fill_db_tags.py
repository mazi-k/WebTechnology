from django.core.management.base import BaseCommand
from app.models import Tag
from faker import Faker

fake = Faker()


class Command(BaseCommand):
    help = u'Filling the database with synthetic tags'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help=u'tags_sum')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        for i in range(total):
            tag = Tag.objects.create(name=fake.word()[:10])
