from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, logout as auth_logout


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


def logout(request):
    auth_logout(request)
    return redirect('/')
