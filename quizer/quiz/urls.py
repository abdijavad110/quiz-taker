from django.urls import path, include
from .views import index, upload, delete


urlpatterns = [
    path('questions', index, name='quiz_main'),
    path('upload', upload, name='upload'),
    path('delete', delete, name='delete'),
]
