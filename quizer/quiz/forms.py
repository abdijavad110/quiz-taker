from django import forms


class AnswerForm(forms.Form):
    answerFile = forms.FileField()
