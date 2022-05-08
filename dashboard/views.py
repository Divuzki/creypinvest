from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from django_countries import countries
from users.models import Wallet, Profile


def dashboard_home_view(request):
    if request.user.is_authenticated:
        if not Wallet.objects.filter(user=request.user.profile):
            Wallet.objects.create(user=request.user.profile)
        qs = Wallet.objects.filter(user=request.user.profile).first()
        bal = qs.balance.split(".")
        first_bal = bal[0]
        second_bal = bal[1]
        context = {
            "title": "Dashboard",
            "crumbs": ["Dashboard"],
            "bal": qs.balance,
            "first_bal": first_bal,
            "second_bal": second_bal,
            "crumbs_count": 1
        }
        return render(request, "dashboard/dashboard_home.html", context)
    else:
        redirect("/auth/account/login?next=/dashboard/")


def dashboard_profile_view(request):
    if request.user.is_authenticated:
        if not Wallet.objects.filter(user=request.user.profile):
            Wallet.objects.create(user=request.user.profile)
        context = {
            "title": "Profile",
            "crumbs": ["Profile"],
            "crumbs_count": 2,
            "countries": countries
        }
        return render(request, "dashboard/dashboard_profile.html", context)
    else:
        redirect("/auth/account/login?next=/dashboard/profile/")


def dashboard_profile_auth_view(request):
    if request.method == "POST":
        form = request.POST
        profile_image = form.get("profile_image")
        if 'profile_image' in request.FILES:
            profile_image = request.FILES['profile_image']
        full_name = form.get("full_name")
        email = form.get("email").strip()
        phone_number = form.get("phone_number").strip()
        gender = form["gender"]
        country = form["country"]

        user = request.user
        user_ = User.objects.filter(username=user.username).first()
        user_profile = Profile.objects.filter(user=user).first()
        if full_name:
            full_name = full_name.split(" ")
            for name in full_name:
                full_name.append(name.strip())
            if full_name[0]:
                user_.first_name = full_name[0]
                user_profile.first_name = full_name[0]
            if full_name[1]:
                user_.last_name = full_name[1]
                user_profile.last_name = full_name[1]
            else:
                pass
        else:
            user_.first_name = ""
            user_profile.first_name = ""

            user_.last_name = ""
            user_profile.last_name = ""

        user_.email = email

        # deleting old uploaded image.
        # image_path = user_profile.image
        # if os.path.exists(image_path):
        #     os.remove(image_path)

        user_profile.email = email
        user_profile.image = profile_image
        user_profile.phone_number = phone_number
        user_profile.gender = gender
        user_profile.country = country

        user_.save()
        user_profile.save()

        return redirect("/dashboard/profile/?success=yes&msg=your+profile+has+been+updated")
    return redirect("dashboard-profile")


def dashboard_referral_view(request):
    if request.user.is_authenticated:
        if not Wallet.objects.filter(user=request.user.profile):
            Wallet.objects.create(user=request.user.profile)
        context = {
            "title": "Referral",
            "crumbs": ["Referral"],
            "crumbs_count": 2
        }
        return render(request, "dashboard/dashboard_referral.html", context)
    else:
        redirect("/auth/account/login?next=/dashboard/referral/")


def dashboard_payments_view(request):
    if request.user.is_authenticated:
        if not Wallet.objects.filter(user=request.user.profile):
            Wallet.objects.create(user=request.user.profile)
        context = {
            "title": "Payments",
            "crumbs": ["Payments"],
            "crumbs_count": 2
        }
        return render(request, "dashboard/dashboard_payments.html", context)
    else:
        redirect("/auth/account/login?next=/dashboard/payments/")
