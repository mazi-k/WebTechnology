from django.shortcuts import render


QUESTIONS = [
    {
        'id': i,
        'title': f'Question {i}',
        'content': f'Long lorem ipsum {i}'
    } for i in range(10)
]

TAGS = [
    {
        'id': i,
        'tag': f'tag {i}'
    } for i in range(3)
]


def index(request):
    questions = [
        {
            'id': i,
            'title': f'Question {i}',
            'content': f'Long lorem ipsum {i}'
        } for i in range(10)
    ]

    return render(request, 'index.html', {'questions': questions, 'tags': TAGS})


def login(request):
    return render(request, 'login.html')


def ask(request):
    return render(request, 'ask.html')


def by_tag(request, tag_id):
    item_tag = TAGS[tag_id]
    return render(request, 'by_tags.html', {'tag': item_tag, 'questions': QUESTIONS, 'tags': TAGS})


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
