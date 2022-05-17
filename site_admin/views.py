from django.shortcuts import render, redirect
from users.models import AdminTransaction as AT, Wallet
from creyp.utils import send_alert_mail


def index_view(request):
    return render(request, "site/admin/index.html")


def transaction_deposit_view(request):
    user = request.user
    if user.is_authenticated:
        qs = AT.objects.all()
        return render(request, "site/admin/admin-deposit.html", {"objects": qs})
    else:
        return render(request, "pages/index.html")


def transaction_del_view(request, id):
    qs = AT.objects.filter(id=id).first()
    if not qs is None:
        try:
            user_email = qs.wallet.user.user.email
            amount = qs.amount
            url = request.build_absolute_uri('/dashboard/')
            html_msg = f'<a href="{url}" class="rounded-pill border">Dashboard</a>'
            send_alert_mail(request, email_subject="Deposit Request Rejected",
                            user_email=user_email, email_message=f"Your Deposit Request For ${amount} Has Been Declined", email_image="transaction-declined.png", html_message=html_msg)
        except:
            pass
        qs.delete()
        return redirect("admin-transaction-deposit")


def transaction_accept_view(request, id):
    qs = AT.objects.filter(id=id).first()
    qsr = Wallet.objects.filter(user=qs.wallet.user).first()
    if not qs is None and not qsr is None:
        try:
            user_email = qs.wallet.user.user.email
            amount = qs.amount
            url = request.build_absolute_uri('/dashboard/')
            html_msg = f'<a href="{url}" class="rounded-pill border">Dashboard</a>'
            send_alert_mail(request, email_subject="Deposit Request Accepted",
                            user_email=user_email, email_message=f"Your Account Has Been Credited ${amount}",
                            email_image="transaction-accept.png", html_message=html_msg)
        except:
            pass
        qsr.balance = float(qsr.balance) + float(qs.amount)
        qsr.save()
        qs.delete()
        return redirect("admin-transaction-deposit")
