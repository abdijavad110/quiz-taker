from django.shortcuts import render, redirect
from .models import Question, Assignments
from persian import convert_en_numbers as pers
from .conf import get_time
from .models import Answer
from datetime import datetime


# Create your views here.
def index(request):
    START_TIME, STOP_TIME = get_time()
    if not request.user.is_authenticated:
        return redirect('login')

    if datetime.now() < START_TIME:
        diff = START_TIME - datetime.now()
        diff = int(diff.total_seconds())
        minutes = diff // 60
        seconds = diff % 60
        return render(request, 'soon.html', {'min': minutes, 'sec': seconds})
    elif datetime.now() >= STOP_TIME:
        return render(request, 'late.html')

    try:
        questions = Assignments.objects.get(user=request.user.id).questions.all()
    except Exception:
        questions = []
    questions = [(
        pers(str(i + 1)),
        q.text,
        (q.pic.url if q.pic.name != '' else ''),
        ("w3-light-grey" if i % 2 else ""),
        q.id,
        ) for i, q in enumerate(questions)]
    answers = [
        (i + 1, ans.id, ans.file.url)
        for i, ans in
        enumerate(Answer.objects.filter(responder=request.user).all())
    ]
    context = {'questions': questions, 'answers': answers}
    return render(request, 'quiz_page.html', context)


def upload(request):
    START_TIME, STOP_TIME = get_time()
    if datetime.now() > STOP_TIME:
        return render(request, 'late.html')

    if request.method == 'POST':
        user = request.user
        file = None
        try:
            file = request.FILES['answer']
        except KeyError:
            pass

        if file is not None:
            ans = Answer()
            ans.file = file
            ans.file.name = str(user.id) + "_" + ans.file.name
            ans.responder = user
            ans.save()

    return redirect('/')


def delete(request):
    START_TIME, STOP_TIME = get_time()
    if datetime.now() > STOP_TIME:
        return render(request, 'late.html')

    if request.method == 'POST':
        ans_id = request.POST['ans_id']
        Answer.objects.filter(id=ans_id).delete()

    return redirect('/')
