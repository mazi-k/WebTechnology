from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .models import Question, Answer, Tag, get_best_members, get_popular_tags, Profile
from .forms import LoginForm, RegisterForm, SettingsForm


def paginate(objects, page, per_page=10):
    paginator = Paginator(objects, per_page)
    return paginator.page(page)


def errors_catcher(page_list, page):
    try:
        questions = paginate(page_list, page)
    except PageNotAnInteger:
        questions = paginate(page_list, 1)
    except EmptyPage:
        questions = paginate(page_list, 1)
    return questions


def index(request):
    page = request.GET.get('page', 1)
    questions = errors_catcher(Question.objects.new_questions(), page)

    return render(request, 'index.html', {'questions': questions,
                                          'popular_tags': get_popular_tags(),
                                          'best_members': get_best_members()})


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def log_in(request):
    if request.method == "GET":
        user_form = LoginForm()
    if request.method == "POST":
        user_form = LoginForm(request.POST)
        if user_form.is_valid():
            user = auth.authenticate(request=request, **user_form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(reverse('index'))
            else:
                user_form.add_error(field=None, error="Wrong username or password")
    return render(request, 'login.html', {'form': user_form,
                                          'popular_tags': get_popular_tags(),
                                          'best_members': get_best_members()})


def ask(request):
    return render(request, 'ask.html', {'popular_tags': get_popular_tags(),
                                        'best_members': get_best_members()})


def by_tag(request, tag_id):
    page = request.GET.get('page', 1)
    tag = Tag.objects.get(id=tag_id)
    questions_by_tag = errors_catcher(Question.objects.tag_questions(tag), page)

    return render(request, 'by_tags.html', {'tag': tag,
                                            'questions': questions_by_tag,
                                            'popular_tags': get_popular_tags(),
                                            'best_members': get_best_members()})


def question(request, question_id):
    question_item = get_object_or_404(Question.objects.questions(), pk=question_id)
    answers = Answer.objects.hot_answers().filter(question_id=question_id)

    return render(request, 'question.html', {'question': question_item,
                                             'answers': answers,
                                             'popular_tags': get_popular_tags(),
                                             'best_members': get_best_members()})


@login_required(login_url="login", redirect_field_name="continue")
@require_http_methods(['GET', 'POST'])
def settings(request):
    if request.method == "GET":
        initial_data = model_to_dict(request.user)
        user_form = SettingsForm(initial=initial_data)

    if request.method == 'POST':
        user_form = SettingsForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid():
            Profile.objects.get_or_create(user=request.user)
            user_form.save()
            return redirect(reverse('index'))
        else:
            user_form.add_error(field=None, error="Invalid POST data")

    return render(request, 'settings.html',
                  {'form': user_form, 'best_members': get_best_members(), 'popular_tags': get_popular_tags()})


@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.method == "GET":
        user_form = RegisterForm()

    if request.method == 'POST':
        user_form = RegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user = user_form.save()
            if user:
                return redirect(reverse('login'))
            else:
                user_form.add_error(field=None, error="User saving error")

    return render(request, 'signup.html', {'form': user_form,
                                           'popular_tags': get_popular_tags(),
                                           'best_members': get_best_members()})


def hot_questions(request):
    page = request.GET.get('page', 1)
    questions = errors_catcher(Question.objects.hot_questions(), page)

    return render(request, 'hot.html', {'questions': questions,
                                        'popular_tags': get_popular_tags(),
                                        'best_members': get_best_members()})


@login_required
def logout_view(request):
    auth.logout(request)
    return redirect(reverse('index'))
