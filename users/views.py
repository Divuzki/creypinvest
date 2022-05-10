from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from users.models import AdminWallet, Profile, Wallet
from users.decorators import update_user_ip
from creyp.utils import send_alert_mail

starter = ["5,000", "4,000", "3,000", "2,000", "1,000", "500"]
etfs = ["15,000", "14,000", "13,000", "12,000", "11,000", "10,000"]


@update_user_ip
def deposit(request):
    user = request.user
    context = {"type": "Deposit Now", "crumbs": ["Deposit Now"]}
    if user.is_authenticated:
        return render(request, "auth/deposit/deposit.html", context)
    else:
        return redirect("/auth/account/login/?next=/auth/deposit/")


@update_user_ip
def deposit_amount(request, pack):
    user = request.user
    if user.is_authenticated:
        price_list = None
        large = False
        if pack == "starter":
            price_list = starter
        elif pack == "exchange-traded-funds":
            price_list = etfs
        else:
            if price_list == None:
                large = True
        context = {
            "pack": pack,
            "price_list": price_list,
            "large": large
        }
        return render(request, "auth/deposit/deposit_amount.html", context)
    else:
        return redirect("/auth/account/login/?next=/auth/deposit/" + str(pack) + "/")


@update_user_ip
def deposit_amount_auth(request, pack):
    context = {"crumbs": ["Deposit Now",
                          "Select Amount", "Checkout"], "type": "Checkout"}
    if request.method == "POST":
        price = request.POST.get("price")
        checkprice = int(price.replace(",", ""))
        if pack == 'starter':
            if checkprice < 500:
                return redirect("deposit")
        if pack == 'exchange-traded-funds':
            if checkprice < 10_000:
                return redirect("deposit")
        if pack == 'expert-trader':
            if checkprice < 25_000:
                return redirect("deposit")
        display_price = price
        price = str(price).replace("$", "").replace(",", "")
        admin_btc_address = AdminWallet.objects.all()

        admin_btc_address = admin_btc_address.first()
        display_price = display_price
        raw_price = int(price)
        context = {"raw_price": raw_price, "display_price": display_price, "btc_address": admin_btc_address, "plan": pack, "crumbs": ["Deposit Now",
                                                                                                                                      "Select Amount", "Checkout"], "type": "Checkout"}
        return render(request, "auth/deposit/deposit_checkout.html", context)
    else:
        return redirect("deposit")


@update_user_ip
def deposit_window(request):
    user = request.user
    if request.method == "POST" and user.is_authenticated:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        pin1 = request.POST.get("pin1")
        pin2 = request.POST.get("pin")
        price = request.POST.get("price")
        profile = Profile.objects.filter(user=user).first()
        wallet = Wallet.objects.filter(user=profile).first()
        user_ = User.objects.filter(username=user.username).first()
        admin_btc_address = AdminWallet.objects.all()
        admin_btc_address = admin_btc_address.first()

        context = {
            "price": price,
            "btc_address": admin_btc_address
        }

        if pin1 and pin2:
            if pin1 == pin2:
                wallet.pin = pin2
                wallet.save()
            else:
                error = "Pins Must Be The Same"
        else:
            error = "Pin Can't Be Empty"

        if error:
            context = {
                "price": price,
                "btc_address": admin_btc_address,
                "error": error
            }

        if first_name:
            user_.first_name = first_name
            profile.first_name = first_name
            user_.save()
            profile.save()

        if last_name:
            user_.last_name = last_name
            profile.last_name = last_name
            user_.save()
            profile.save()

        try:
            send_alert_mail(request=request, email_subject="Payment Window Has Been Opened", user_email=request.user.email,
                            email_message=f"A Payment Window Has Been Initiated, Please Complete Your Deposit Process", email_image="payment-window.png")
        except:
            pass
        return render(request, "auth/deposit/deposit_paying.html", context)
    else:
        return redirect("deposit")
