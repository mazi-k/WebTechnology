from django.core.management.base import BaseCommand
import random
from app.models import *
from faker import Faker

fake = Faker()


class Command(BaseCommand):
    help = u'Filling the database with synthetic questions'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help=u'questions_sum')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        author_list = Profile.objects.all()
        tag_list = Tag.objects.values_list('id', flat=True)

        for i in range(total):
            question = Question.objects.create(
                title=fake.sentence(),
                content=fake.text()[:1024],
                author=random.choice(author_list))

            for j in range(random.randint(1, 5)):
                tag = random.choice(tag_list)
                question.tag.add(tag)
