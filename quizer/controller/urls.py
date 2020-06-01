from django.urls import path
from .views import time, index, assign, grade


urlpatterns = [
    path('', index),
    path('time', time),
    path('assign', assign),
    path('grade', grade),
]
