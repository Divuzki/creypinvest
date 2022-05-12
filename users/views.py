from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from users.models import AdminWallet, Profile, Wallet, Transaction, AdminTransaction
from users.decorators import update_user_ip
from creyp.utils import send_alert_mail, set_cookie_function, random_string_generator

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
        qs = Transaction.objects.create(wallet=request.user.profile.wallet, transactionId=random_string_generator(size=17).upper(), amount=price,
                                        status="pending", msg=f"Initial price at ${price} is pending")
        qs.save()
        _hash = qs.hash_id
        transactionId = qs.transactionId
        res = render(request, "auth/deposit/deposit_checkout.html", context)
        set_cookie_function("pending_hash", str(_hash),
                            max_age=500*1900, response=res)
        set_cookie_function("pending_hash_id", str(transactionId),
                            max_age=1*24*60*60*1000, response=res)
        return res
    else:
        return redirect("deposit")


@update_user_ip
def deposit_window(request):
    user = request.user
    if request.method == "POST" and user.is_authenticated:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        pin1 = request.POST.get("pin1")

        plan = request.POST.get("plan")

        price = request.POST.get("price")
        price_btc = request.POST.get("price_btc")

        price_fees = request.POST.get("price_fees")
        price_fees_btc = request.POST.get("price_fees_btc")

        price_total = request.POST.get("price_total")
        price_total_btc = request.POST.get("price_total_btc")

        profile = Profile.objects.filter(user=user).first()
        wallet = Wallet.objects.filter(user=profile).first()
        user_ = User.objects.filter(username=user.username).first()
        admin_btc_address = AdminWallet.objects.all()
        admin_btc_address = admin_btc_address.first()

        context = {
            "plan": plan,
            "price": price,
            "price_btc": price_btc,
            "price_fees": price_fees,
            "price_fees_btc": price_fees_btc,
            "price_total": price_total,
            "price_total_btc": price_total_btc,
            "btc_address": admin_btc_address
        }
        error = None
        if pin1 == None:
            error = "Pin Can't Be Empty"

        else:
            wallet.pin = pin1
            wallet.save()

        if not error == None:
            context = {
                "plan": plan,
                "price": price,
                "price_btc": price_btc,
                "price_fees": price_fees,
                "price_fees_btc": price_fees_btc,
                "price_total": price_total,
                "price_total_btc": price_total_btc,
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

        pending_hash = request.COOKIES.get("pending_hash", None) == None
        res = render(request, "auth/deposit/deposit_window.html", context)
        if not pending_hash == True and not price_total:
            _hash = request.COOKIES['pending_hash_id']
            qs = Transaction.objects.filter(transactionId=_hash).first()
            qs.amount = price_total
            qs.status = "processing"
            _hash = qs.hash_id
            qs.msg = f"Total Price at ${price_total} is been processed"
            transactionId = qs.transactionId
            qs.save()
        else:
            qs = Transaction.objects.create(
                wallet=wallet, amount=price, status="processing", transactionId=random_string_generator(size=17).upper(), msg=f"${price_total} is been processed")
            qs.save()
            _hash = qs.hash_id
            transactionId = qs.transactionId
        set_cookie_function("pending_hash", str(_hash),
                            max_age=1*24*60*1000, response=res)
        set_cookie_function("pending_hash_id", str(transactionId),
                            max_age=1*24*60*60*1000, response=res)
        try:
            send_alert_mail(request=request, email_subject="Payment Window Has Been Opened", user_email=request.user.email,
                            email_message=f"A Payment Window Has Been Initiated, Please Complete Your Deposit Process", email_image="payment-window.png")
        except:
            pass
        return res
    else:
        return redirect("deposit")


def deposit_done(request, plan):
    user = request.user
    profile = user.profile
    wallet = profile.wallet

    if request.method == "POST":
        form = request.POST
        price = form.get("total_price")
        btc_address = form.get("user_bitcoin_address")
        make_default = form.get("make_default")

        if btc_address == None or btc_address == '':
            btc_address = wallet.btc_address
        if make_default:
            qs = Wallet.objects.filter(user=profile).first()
            qs.btc_address = btc_address
            qs.save()
        pending_hash = request.COOKIES.get("pending_hash", None) == None
        transactionId = request.COOKIES.get("pending_hash_id", None) == None
        if not transactionId == True and not pending_hash == None:
            pending_hash = request.COOKIES['pending_hash']
            transactionId = request.COOKIES['pending_hash_id']
            qs = Transaction.objects.filter(
                wallet=wallet, hash_id=pending_hash, transactionId=transactionId).first()
            if not qs is None and not price == None:
                qs.status = "confirming"
                qs.msg = f"You deposit request of ${price} is been confirmed"
                qs.save()
                # btc_address = wallet.btc_address
                qsr = AdminTransaction.objects.filter(wallet=wallet, transactionId=transactionId).first()
                if qsr is None:
                    qsr = AdminTransaction.objects.create(wallet=wallet, plan=plan, amount=price, transactionId=transactionId, btc_address=btc_address,
                                                          msg=f"Username: {user.username}, Bitcoin Address: {btc_address}, Money Transfered: {price}")
                    qsr.save()
                    try:
                        send_alert_mail(request=request, email_subject=f"${price} Deposit Requested", user_email="divuzki@gmail.com",
                                        email_message=f"User `{user.username}` deposited ${price} and its undergoing confirmation by the team team. It will take 1-3 days before he/she get credited", email_image="user-payed.png")
                    except:
                        pass
                try:
                    send_alert_mail(request=request, email_subject="Payment Window Has Been Closed", user_email=request.user.email,
                                    email_message=f"A Payment Window Has Been Closed, Hope You Transfered ${price} To {btc_address} Deposit Process", email_image="payment-window-closed.png")
                    send_alert_mail(request=request, email_subject=f"${price} Deposit Requested", user_email=request.user.email,
                                    email_message=f"You deposited ${price} and its undergoing confirmation by our team. This will take 1-3 days before you get credited", email_image="deposit-confirming.png")
                except:
                    pass
        else:
            return redirect("/auth/deposit/?e=missing+encrption+please+try+again")
        return render(request, "auth/deposit/deposit_done.html", {"price": price})
    else:
        return redirect("deposit")
