# config/urls.py
from django.contrib import admin
from django.urls import path, include
from .views import index, home, login, signup, logout, profile
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('quiz/', include('quiz.urls')),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('', index, name='home'),
                  path('test/', home),
                  path('login/', login, name='login'),
                  path('signup/', signup, name='signup'),
                  path('logout/', logout, name='logout'),
                  path('profile/', profile, name='profile'),
                  path('control/', include('controller.urls')),
              ] + static('/media', document_root=settings.MEDIA_ROOT)
