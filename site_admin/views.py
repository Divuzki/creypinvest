from django.shortcuts import render, redirect
from users.models import AdminTransaction as AT, Wallet, Transaction, Profile
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
    tasc = Transaction.objects.filter(transactionId=qs.transactionId).first()
    if not qs is None:
        try:
            user_email = qs.wallet.user.user.email
            amount = qs.amount
            url = request.build_absolute_uri('/dashboard/')
            html_msg = f'<a style="border: 1px solid #673ab7;padding: 5px 10px;border-radius: 24px;color: #fff;background: #673ab7;" href="{url}" class="rounded-pill border">Dashboard</a>'
            send_alert_mail(request, email_subject="Deposit Request Rejected",
                            user_email=user_email, email_message=f"Your Deposit Request For ${amount} Has Been Declined", email_image="transaction-declined.png", html_message=html_msg)
        except:
            pass
        tasc.status = "failed"
        tasc.msg = f"Your ${qs.amount} Deposit Request Was Rejected"
        tasc.transactionId = qs.transactionId
        tasc.save()
        qs.delete()
        return redirect("admin-transaction-deposit")


def transaction_accept_view(request, id):
    qs = AT.objects.filter(id=id).first()
    qsr = Wallet.objects.filter(user=qs.wallet.user).first()
    tasc = Transaction.objects.filter(transactionId=qs.transactionId).first()
    profile = Profile.objects.filter(user=qs.wallet.user.user).first()
    if not qs is None and not qsr is None:
        try:
            user_email = qs.wallet.user.user.email
            amount = qs.amount
            url = request.build_absolute_uri('/dashboard/')
            html_msg = f'<a href="{url}" style="border: 1px solid #673ab7;padding: 5px 10px;border-radius: 24px;color: #fff;background: #673ab7;" class="rounded-pill border">Dashboard</a>'
            send_alert_mail(request, email_subject="Deposit Request Accepted",
                            user_email=user_email, email_message=f"Your Account Has Been Credited ${amount}",
                            email_image="transaction-accept.png", html_message=html_msg)
        except:
            pass
        tasc.status = "credit"
        tasc.msg = f"Your Account has been credited ${qs.amount}"
        tasc.transactionId = qs.transactionId
        tasc.save()
        qsr.balance = float(qsr.balance) + float(qs.amount)
        qsr.save()
        profile.deposit_before = True
        profile.save()
        qs.delete()
        return redirect("admin-transaction-deposit")