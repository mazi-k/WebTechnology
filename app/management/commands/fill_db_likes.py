from django.core.management.base import BaseCommand

import random
from faker import Faker

fake = Faker()

from app.models import *


class Command(BaseCommand):
    help = u'Filling the database with synthetic likes'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help=u'likes_sum')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        author_list = Profile.objects.all()
        questions_list = Question.objects.all()
        answers_list = Answer.objects.all()

        for i in range(total):
            user = random.choice(author_list)
            question = random.choice(questions_list)
            answer = random.choice(answers_list)

            like_question = LikeQuestion.objects.create(question=question, user=user)
            like_answer = LikeAnswer.objects.create(answer=answer, user=user)
