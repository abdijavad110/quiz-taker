from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Count
from django.contrib.auth.models import User
from datetime import datetime
from quizer.views import _assign_questions
from quiz.models import Assignments, Question, Answer
from .models import Time
from persian import convert_en_numbers as pers


def grade(request):
    if not request.user.is_staff:
        return redirect('login')

    try:
        questions = Assignments.objects.get(user=request.POST['user']).questions.all()
    except Exception:
        questions = []
    users = [(u.id, u.username, u.first_name, u.last_name) for u in User.objects.all()]
    try:
        user = User.objects.get(id=int(request.POST['user'])) if request.POST['user'] is not None else None
    except Exception:
        user = None
    questions = [(
        pers(str(i + 1)),
        q.text,
        (q.pic.url if q.pic.name != '' else ''),
        ("w3-light-grey" if i % 2 else ""),
        q.id,
    ) for i, q in enumerate(questions)]
    try:
        answers = [
            (i + 1, ans.id, ans.file.url)
            for i, ans in
            enumerate(Answer.objects.filter(responder=user.id).all())
        ]
    except:
        answers = []
    context = {'questions': questions, 'answers': answers, 'users': users, 'user': user}
    return render(request, 'control/grading.html', context)


def index(request):
    return redirect('/control/time')  # fixme fix this
    if not request.user.is_staff:
        return HttpResponse("Restricted Access !!!")
    return HttpResponse("well-done!!")


def time(request):
    if not request.user.is_staff:
        return HttpResponse("Restricted Access !!!")

    t = Time.objects.get(active=True)
    if request.method == 'POST':
        args = request.POST

        t.start = datetime(int(args['start_year']), int(args['start_month']), int(args['start_day']),
                           int(args['start_hour']), int(args['start_minute']))
        t.stop = datetime(int(args['stop_year']), int(args['stop_month']), int(args['stop_day']),
                          int(args['stop_hour']), int(args['stop_minute']))
        t.save()
        return redirect('/control/')
    else:
        start, stop = t.start, t.stop
        return render(request, 'control/time.html',
                      {'start_year': start.year, 'start_month': start.month, 'start_day': start.day,
                       'start_hour': start.hour, 'start_minute': start.minute, 'stop_year': stop.year,
                       'stop_month': stop.month, 'stop_day': stop.day, 'stop_hour': stop.hour,
                       'stop_minute': stop.minute})


def assign(request):
    if not request.user.is_staff:
        return HttpResponse("Restricted Access !!!")
    if request.method == 'POST':
        types = request.POST['types']
        types = list(map(int, types.replace(' ', '').split(',')))

        Assignments.objects.all().delete()
        for u in User.objects.all():
            _assign_questions(u.id, types)

        return redirect('/control/')
    else:
        types = set([Question.objects.get(id=e).type for e in
                     Assignments.objects.values_list('questions', flat=True).distinct()])
        ts = ""
        for t in types:
            ts += str(t) + ","
        if ts.endswith(','):
            ts = ts[:-1]
        return render(request, 'control/assign.html', {'types': ts})
