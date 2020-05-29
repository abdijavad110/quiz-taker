from django.urls import path
from .views import time, index, assign


urlpatterns = [
    path('', index),
    path('time', time),
    path('assign', assign),
]
