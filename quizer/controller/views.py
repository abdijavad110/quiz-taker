from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Count
from django.contrib.auth.models import User
from quiz.conf import set_new_time, get_time
from datetime import datetime
from quiz.models import Question, Assignments
from quizer.views import _assign_questions


def index(request):
    return redirect('/control/time')  # fixme fix this
    if not request.user.is_staff:
        return HttpResponse("Restricted Access !!!")
    return HttpResponse("well-done!!")


def time(request):
    if not request.user.is_staff:
        return HttpResponse("Restricted Access !!!")

    if request.method == 'POST':
        args = request.POST

        set_new_time(
            datetime(int(args['start_year']), int(args['start_month']), int(args['start_day']), int(args['start_hour']),
                     int(args['start_minute'])),
            datetime(int(args['stop_year']), int(args['stop_month']), int(args['stop_day']), int(args['stop_hour']),
                     int(args['stop_minute'])))
        return redirect('/control/')
    else:
        start, stop = get_time()
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
