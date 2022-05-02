from django.urls import path, include
from core.views import about, why, process

urlpatterns = [
    path("about", about, name="about"),
    path("why", why, name="why"),
    path("process", process, name="process"),
]
