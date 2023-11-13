from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from .models import Question, Answer, Tag, get_best_members, get_popular_tags


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
                                          'popular_tags': get_popular_tags(),
                                          'best_members': get_best_members()})


def login(request):
    return render(request, 'login.html', {'popular_tags': get_popular_tags(),
                                          'best_members': get_best_members()})


def ask(request):
    return render(request, 'ask.html', {'popular_tags': get_popular_tags(),
                                        'best_members': get_best_members()})


def by_tag(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    by_tag_list = Question.objects.tag_questions(tag)
    page = request.GET.get('page', 1)

    try:
        questions = paginate(by_tag_list, page)
    except PageNotAnInteger:
        questions = paginate(by_tag_list, 1)
    except EmptyPage:
        questions = paginate(by_tag_list, 1)

    return render(request, 'by_tags.html', {'tag': tag,
                                            'questions': questions,
                                            'popular_tags': get_popular_tags(),
                                            'best_members': get_best_members()})


def question(request, question_id):
    question_item = get_object_or_404(Question.objects.questions(), pk=question_id)
    answers = Answer.objects.hot_answers().filter(question_id=question_id)

    return render(request, 'question.html', {'question': question_item,
                                             'answers': answers,
                                             'popular_tags': get_popular_tags(),
                                             'best_members': get_best_members()})


def settings(request):
    return render(request, 'settings.html', {'popular_tags': get_popular_tags(),
                                             'best_members': get_best_members()})


def signup(request):
    return render(request, 'signup.html', {'popular_tags': get_popular_tags(),
                                           'best_members': get_best_members()})


def hot_questions(request):
    page = request.GET.get('page', 1)
    page_list = Question.objects.hot_questions()

    try:
        questions = paginate(page_list, page)
    except PageNotAnInteger:
        questions = paginate(page_list, 1)
    except EmptyPage:
        questions = paginate(page_list, 1)

    return render(request, 'hot.html', {'questions': questions,
                                        'popular_tags': get_popular_tags(),
                                        'best_members': get_best_members()})
