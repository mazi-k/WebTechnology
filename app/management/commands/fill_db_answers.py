from django.core.management.base import BaseCommand

import random
from faker import Faker

from app.models import *

fake = Faker()


class Command(BaseCommand):
    help = u'Filling the database with synthetic answers'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help=u'answers_sum')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        author_list = Profile.objects.all()
        questions_list = Question.objects.all()

        for i in range(total):
            author = random.choice(author_list)
            question = random.choice(questions_list)
            answer = Answer.objects.create(answer=fake.text(), question_id=question, author=author)
