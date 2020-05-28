from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Question(models.Model):
    name = models.CharField(max_length=15, default="بی‌نام")
    text = models.TextField(default="", blank=True)
    pic = models.ImageField(upload_to="questions", default=None, blank=True)


class Answer(models.Model):
    file = models.FileField(upload_to="answers")
    responder = models.ForeignKey(User, models.CASCADE)
