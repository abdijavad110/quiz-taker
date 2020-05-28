from django.shortcuts import render, redirect
from .models import Question
from persian import convert_en_numbers as pers
from .forms import AnswerForm
from .models import Answer
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect('login')

    questions = Question.objects.all()
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
    if request.method == 'POST':
        user = request.user
        file = None
        try:
            file = request.FILES['answer']
        except KeyError:
            pass
        question = request.POST['question']

        if file is not None:
            ans = Answer()
            ans.file = file
            ans.file.name = str(user.id) + "_" + ans.file.name
            ans.question = Question.objects.get(id=question)
            ans.responder = user
            ans.save()

    return redirect('/')


def delete(request):
    if request.method == 'POST':
        ans_id = request.POST['ans_id']
        Answer.objects.filter(id=ans_id).delete()

    return redirect('/')
