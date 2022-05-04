from django.urls import path
from core.views import about, contact

urlpatterns = [
    path("about-us/", about, name="about-us"),
    path("contact-us/", contact, name="contact-us"),
]
