from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from .models import Question, Answer, get_best_members, get_popular_tags


QUESTIONS = [
    {
        'id': i,
        'title': f'Question {i}',
        'content': f'Long lorem ipsum {i}'
    } for i in range(35)
]

TAGS = [
    {
        'id': i,
        'tag': f'tag {i}'
    } for i in range(3)
]


def paginate(objects, page, per_page=10):
    paginator = Paginator(objects, per_page)
    return paginator.page(page)


def index(request):
    page = request.GET.get('page', 1)
    page_list = Question.objects.new_questions()

    try:
        questions = paginate(page_list, page)
    except PageNotAnInteger:
        questions = paginate(page_list, 1)
    except EmptyPage:
        questions = paginate(page_list, 1)

    return render(request, 'index.html', {'questions': questions,
                                          'tags': get_popular_tags(),
                                          'users': get_best_members()})


def login(request):
    return render(request, 'login.html')


def ask(request):
    return render(request, 'ask.html')


def by_tag(request, tag_id):
    item_tag = TAGS[tag_id]
    page = request.GET.get('page', 1)

    try:
        questions = paginate(QUESTIONS, page)
    except PageNotAnInteger:
        questions = paginate(QUESTIONS, 1)
    except EmptyPage:
        questions = paginate(QUESTIONS, 1)

    return render(request, 'by_tags.html', {'tag': item_tag, 'questions': questions, 'tags': TAGS})


def question(request, question_id):
    answers = [
        {
            'id': i,
            'content': f'This is answer {i}',
            'is_correct': True
        } for i in range(3)
    ]

    item = QUESTIONS[question_id]

    return render(request, 'question.html', {'question': item, 'answers': answers, 'tags': TAGS})


def settings(request):
    return render(request, 'settings.html')


def signup(request):
    return render(request, 'signup.html')


def hot_questions(request):
    page = request.GET.get('page', 1)
    page_list = Question.objects.hot_questions()

    try:
        questions = paginate(page_list, page)
    except PageNotAnInteger:
        questions = paginate(page_list, 1)
    except EmptyPage:
        questions = paginate(page_list, 1)

    return render(request, 'hot.html', {'questions': questions, 'tags': TAGS})
