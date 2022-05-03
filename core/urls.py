from django.urls import path, include
from core.views import about, why, process

urlpatterns = [
    path("about-us/", about, name="about-us"),
    path("contact-us/", process, name="contact-us"),
]
