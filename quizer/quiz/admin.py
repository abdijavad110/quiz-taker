from django.contrib import admin
from .models import Question, Answer, Assignments


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('type', 'name', 'text', 'pic',)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('responder', 'file', 'time')


class AssignAdmin(admin.ModelAdmin):
    list_display = ('user',)


# Register your models here.
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Assignments, AssignAdmin)
