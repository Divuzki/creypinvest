from django.urls import path
from dashboard.views import dashboard_home_view

urlpatterns = [
    path('', dashboard_home_view, name="dashboard-home")
]