from django.urls import path
from .views import time, index


urlpatterns = [
    path('', index),
    path('time', time),
]
