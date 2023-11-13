from django.core.management.base import BaseCommand

from app.management.commands import fill_db_tags, fill_db_questions
from app.management.commands import fill_db_users, fill_db_answers, fill_db_likes


class Command(BaseCommand):
    help = u'Filling database with synthetic data'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help=u'multi')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        fill_db_users.Command.handle(self, *args, **kwargs)
        fill_db_tags.Command.handle(self, *args, **kwargs)
        kwargs['total'] = total*10
        fill_db_questions.Command.handle(self, *args, **kwargs)
        kwargs['total'] = total * 100
        fill_db_answers.Command.handle(self, *args, **kwargs)
        kwargs['total'] = total * 100
        fill_db_likes.Command.handle(self, *args, **kwargs)
