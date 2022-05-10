from django.urls import path
from .views import deposit, deposit_amount, deposit_amount_auth, deposit_window

urlpatterns = [
    path("deposit/", deposit, name="deposit"),
    path("deposit/<str:pack>/", deposit_amount, name="deposit_amount"),
    path("deposit/<str:pack>/auth/", deposit_amount_auth, name="deposit_amount_auth"),
    path("deposit/auth/start-window/", deposit_window, name="deposit_window"),
    # path("deposit/<str:pack>/auth/paying", deposit_amount_auth, name="deposit_amount_auth"),
    # deposit_amount_auth
]
