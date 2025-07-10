from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('attendance.urls')),  # your existing attendance app
    path('chat/', include('chatting.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf.urls import handler404
from django.shortcuts import render

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

handler404 = custom_404_view
handler500 = 'django.views.defaults.server_error'
