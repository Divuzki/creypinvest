from django.urls import path
from .views import deposit, depositing

urlpatterns = [
    path("deposit/", deposit, name="deposit"),
    path("deposit/<int:price>/", depositing, name="dp-price"),
]
