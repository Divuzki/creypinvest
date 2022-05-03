from django.urls import path
from .views import deposit, depositing, signup, login_view, activation_sent_view, activate

urlpatterns = [
    path("account/login/", login_view, name="login"),
    path("register/", signup, name="register"),
    path("account/signup/", signup, name="signup"),
    path("deposit/", deposit, name="deposit"),
    path("deposit/<int:price>/", depositing, name="dp-price"),

    path('email/sent/', activation_sent_view, name="activation_sent"),
    path('email/activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
]
