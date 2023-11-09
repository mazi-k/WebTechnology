from django.core.paginator import Paginator
from django.shortcuts import render


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

    return render(request, 'index.html', {'questions': paginate(QUESTIONS, page), 'tags': TAGS})


def login(request):
    return render(request, 'login.html')


def ask(request):
    return render(request, 'ask.html')


def by_tag(request, tag_id):
    item_tag = TAGS[tag_id]
    page = request.GET.get('page', 1)
    return render(request, 'by_tags.html', {'tag': item_tag, 'questions': paginate(QUESTIONS, page), 'tags': TAGS})


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
    return render(request, 'hot.html', {'questions': paginate(QUESTIONS, page), 'tags': TAGS})
