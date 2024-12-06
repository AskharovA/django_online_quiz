from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    re_path(r'^oauth/', include('social_django.urls', namespace='social')),
    path('admin/', admin.site.urls),
    path('', include('app.main.urls', namespace='main')),
    path('game/', include('app.game.urls', namespace='game')),
    path('users/', include('app.users.urls', namespace='users')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
