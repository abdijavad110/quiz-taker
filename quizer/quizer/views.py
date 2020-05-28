from django.shortcuts import redirect, render
from django.contrib.auth.models import User


def index(request):
    return redirect('quiz/questions')


def home(request):
    return render(request, 'home.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.get(username=username)
