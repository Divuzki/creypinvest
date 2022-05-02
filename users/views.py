from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.utils.encoding import force_str as force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
# from django.conf import settings

from .tokens import account_activation_token
from .forms import SignUpForm
from .tokens import account_activation_token
# from users.models import Profile
from users.utils import send_activate_email


def deposit(request):
    user = request.user
    if user.is_authenticated:
        return render(request, "auth/deposit.html")
    else:
        return redirect("/auth/account/login/")


def login_view(request):
    context = {"type": "Login"}
    if request.method == "GET":
        e = request.GET.get("e")
        if e:
            context = {"type": "Login", "e": e}
        return render(request, "auth/login.html", context)

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        qs = User.objects.get(username__exact=qs.username)
        if qs is not None:
            password = qs.check_password(qs.password)
            username = qs.username
            print(qs.password)
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return redirect("/auth/deposit")
        else:
            return redirect("/auth/account/login/?e=Invalid+user+information!")
    else:
        return redirect("/auth/account/login/?e=User+not+found")
    return render(request, "auth/login.html", context)


def depositing(request, price):
    user = request.user
    if user.is_authenticated:
        if price == 10000 or price == 15000 or price == 20000 or price == 25000:
            if request.method == "POST":
                context = {
                    "depositing": "yes",
                    "price": price,
                    "type": "Deposited"
                }
            else:
                context = {
                    "depositing": "yes",
                    "price": price,
                    "type": "Depositing"
                }
        else:
            context = {
                "depositing": "no"
            }
        return render(request, "auth/deposit.html", context)
    else:
        return redirect("/auth/account/login/")


def activation_sent_view(request):
    return render(request, 'auth/activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true
        user.is_active = True
        # set signup_confirmation true
        user.profile.signup_confirmation = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'auth/activation_invalid.html')


def signup(request):
    form = SignUpForm()  # Django User Creation Form
    nxt = request.GET.get('next')

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.email = form.cleaned_data.get('email')
            # user can't login until link confirmed
            user.is_active = False
            user.save()
            try:
                send_activate_email(user, request, nxt)
                return redirect('activation_sent')
            except:
                username = request.POST.get('username').lower()
                password = request.POST.get('password')
                user = authenticate(
                    request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    if nxt:
                        return redirect(f"/{nxt}")
                    else:
                        return redirect("/auth/deposit")
    context = {
        "form": form,
        "type": "SignUp",
        "nxt": nxt,
        "title": "Create A New Investor Account"
    }
    return render(request, "auth/signup.html", context)
