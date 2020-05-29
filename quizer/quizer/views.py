from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, logout as auth_logout
from quiz.models import Assignments, Question
from random import choice, shuffle


def index(request):
    return redirect('quiz/questions')


def home(request):
    return render(request, 'home.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('/')

    errors = []
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('/')
        else:
            errors.append("نام‌کاربری یا گذرواژه صحیح نمی‌باشد.")
    return render(request, "registration/login.html", {'errors': errors})


def signup(request):
    if request.user.is_authenticated:
        return redirect('/')

    errors = []
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        password_rep = request.POST['password_rep']
        f_name = request.POST['first_name']
        l_name = request.POST['last_name']

        if User.objects.filter(username=username).exists():
            errors.append("نام کاریری موردنظر قبلا استفاده‌شده است. از نام کاربری دیگری استفاده کنید.")
        if len(password) < 5:
            errors.append("گذرواژه انتخابی شما باید حداقل از ۶ حرف یا عدد تشکیل شده‌باشد.")
        if password != password_rep:
            errors.append("گذرواژه‌های وارد شده با هم تطابق ندارند.")
        if f_name == "":
            errors.append("وارد کردن نام اجباریست.")
        if l_name == "":
            errors.append("وارد کردن نام‌خانوادگی اجباریست.")
        if len(errors) == 0:
            user = User.objects.create_user(username, password=password)
            user.last_name = l_name
            user.first_name = f_name
            user.save()

            auth_login(request, user)
            return redirect('/')
    return render(request, 'registration/signup.html', {'errors': errors})


def _assign_questions(user_id, types):
    assignment = Assignments(user=User.objects.get(id=user_id))
    assignment.save()

    shuffle(types)

    for i in types:
        qs = Question.objects.filter(type=i).all()
        assignment.questions.add(choice(qs))

    assignment.save()


def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('/')


def profile(request):

    if not request.user.is_authenticated:
        return redirect('/login/')
    else:
        user = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        f_name = request.POST['f_name']
        l_name = request.POST['l_name']

        if f_name == "" or l_name == "":
            return render(request, 'registration/profile.html',
                          {'errors': ["نام و نام‌خانوادگی نباید خالی باشند."],
                           'names': {
                           'f_name': user.first_name,
                           'l_name': user.last_name
                           }})

        user.first_name = f_name
        user.last_name = l_name
        user.save()
        return redirect('/')
    else:
        return render(request, 'registration/profile.html',
                      {'errors': [],
                       'names': {
                           'f_name': user.first_name,
                           'l_name': user.last_name
                       }})
