# config/urls.py
from django.contrib import admin
from django.urls import path, include
from .views import index, home
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('quiz/', include('quiz.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', index, name='home'),
    path('test/', home)
] + static('/media', document_root=settings.MEDIA_ROOT)

