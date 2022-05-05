from django.urls import path
from .views import deposit, deposit_amount, deposit_amount_auth

urlpatterns = [
    path("deposit/", deposit, name="deposit"),
    path("deposit/<str:pack>/", deposit_amount, name="deposit_amount"),
    path("deposit/<str:pack>/auth/", deposit_amount_auth, name="deposit_amount_auth"),
    # deposit_amount_auth
]
