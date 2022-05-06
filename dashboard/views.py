from django.shortcuts import render

def dashboard_home_view(request):
    return render(request, "dashboard/dashboard_home.html")
