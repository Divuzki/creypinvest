from django.urls import path
from dashboard.views import dashboard_home_view, dashboard_profile_view, dashboard_referral_view, dashboard_profile_auth_view

urlpatterns = [
    path('', dashboard_home_view, name="dashboard-home"),
    path('profile/', dashboard_profile_view, name="dashboard-profile"),
    path('profile/auth/', dashboard_profile_auth_view, name="dashboard-password-update"),
    path('referral/', dashboard_referral_view, name="dashboard-referral"),
]