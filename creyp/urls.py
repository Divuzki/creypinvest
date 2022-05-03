from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('site/', include('core.urls')),
    path('', index, name="home"),
    path('auth/', include('users.urls')),
    path('auth/account/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)