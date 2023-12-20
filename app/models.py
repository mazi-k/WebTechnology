from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count


class Tag(models.Model):
    name = models.CharField(max_length=16, primary_key=True)

    def __str__(self):
        return f'{self.name}'


class ProfileManager(models.Manager):
    def get_users(self):
        return self.get_queryset()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    nickname = models.CharField(max_length=64)
    avatar = models.ImageField()

    objects = ProfileManager()

    def __str__(self):
        return f'{self.user.username}'


class QuestionManager(models.Manager):
    def questions(self):
        return self.get_queryset().order_by('-timestamp').annotate(likes=Count('likequestion', distinct=True))

    def hot_questions(self):
        return self.get_queryset().annotate(answers_count=Count('answer', distinct=True),
                                            likes=Count('likequestion', distinct=True)).order_by('-likes')

    def new_questions(self):
        return self.get_queryset().order_by('-timestamp').annotate(answers_count=Count('answer', distinct=True),
                                                                   likes=Count('likequestion', distinct=True))

    def tag_questions(self, tag):
        return self.get_queryset().filter(tag__name__contains=tag).annotate(
            answers_count=Count('answer', distinct=True),
            likes=Count('likequestion', distinct=True))

    def get_count_questions_by_tag(self, tag):
        return self.get_queryset().filter(tag__name__contains=tag).count()


class Question(models.Model):
    title = models.CharField(max_length=256)
    content = models.CharField(max_length=2048)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    tag = models.ManyToManyField(Tag)

    objects = QuestionManager()

    def __str__(self):
        return f'Question Author {self.author.user.username}'


class AnswerManager(models.Manager):
    def get_count_answers_by_profile(self, profile):
        return self.get_queryset().filter(author__user__username__contains=profile).count()

    def hot_answers(self):
        return self.get_queryset().annotate(likes=Count('likeanswer', distinct=True)).order_by('-likes')


class Answer(models.Model):
    answer = models.CharField(max_length=2048)
    question_id = models.ForeignKey(Question, on_delete=models.PROTECT)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    is_correct = models.BooleanField(default=False)

    objects = AnswerManager()

    def __str__(self):
        return f'Answer Author {self.author.user.username}'


# автоматически промежуточная таблица  не создалась, а с этой таблицей и field tag to question и model QuestionTags
# создались :|
class QuestionTags(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class LikeQuestion(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )


class LikeAnswer(models.Model):
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )


def get_best_members():
    answers_count = {}
    for profile in Profile.objects.all():
        answers_count[profile] = Answer.objects.get_count_answers_by_profile(profile.user.username)
    best_members = sorted(answers_count, key=answers_count.get, reverse=True)[0:5]

    return best_members


def get_popular_tags():
    question_count = {}
    for tag in Tag.objects.all():
        question_count[tag] = Question.objects.get_count_questions_by_tag(tag)
    popular_tags = sorted(question_count, key=question_count.get, reverse=True)[0:6]

    return popular_tags
