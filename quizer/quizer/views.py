from django.shortcuts import redirect, render


def index(request):
    return redirect('quiz/questions')


def home(request):
    return render(request, 'home.html')
