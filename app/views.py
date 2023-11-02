from django.shortcuts import render



def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


def ask(request):
    return render(request, 'ask.html')


def by_tag(request):
    return render(request, 'by_tag.html')


def question(request):
    return render(request, 'question.html')


def settings(request):
    return render(request, 'settings.html')


def signup(request):
    return render(request, 'signup.html')
