from django.urls import path, include
from .views import index, upload


urlpatterns = [
    path('questions', index, name='quiz_main'),
    path('upload', upload, name='upload')
]
