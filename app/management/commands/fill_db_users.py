import os, random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from app.models import Profile

from faker import Faker

fake = Faker()


class Command(BaseCommand):
    help = u'Filling the database with synthetic users'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help=u'users_sum')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        for i in range(total):
            user = User.objects.create_user(
                username=fake.first_name() + str(random.randint(1, 10000)),
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                password='12345678')
            avatar = random.choice(os.listdir("uploads/"))
            profile = Profile.objects.create(user=user, avatar=avatar)
