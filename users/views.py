from django.shortcuts import render, redirect
from users.models import AdminWallet

starter = ["5,000", "4,000", "3,000", "2,000", "1,000", "500"]
etfs = ["15,000", "14,000", "13,000", "12,000", "11,000", "10,000"]


def deposit(request):
    user = request.user
    context = {"type": "Deposit Now", "crumbs": ["Deposit Now"]}
    if user.is_authenticated:
        return render(request, "auth/deposit/deposit.html", context)
    else:
        return redirect("/auth/account/login/?next=/auth/deposit/")


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
