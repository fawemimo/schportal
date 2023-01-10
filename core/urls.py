from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('contmgr/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', include('mainsite.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
