from django.shortcuts import render, redirect


def deposit(request):
    user = request.user
    context = {"type": "Deposit Now", "crumbs": ["Deposit Now"]}
    if user.is_authenticated:
        return render(request, "auth/deposit.html", context)
    else:
        return redirect("account_login")

def depositing(request, price):
    user = request.user
    if user.is_authenticated:
        # context = {"type":"Deposit Now", "crumbs":["Deposit Now"]}
        if price == 10000 or price == 15000 or price == 20000 or price == 25000:
            if request.method == "POST":
                context = {
                    "depositing": "yes",
                    "price": price,
                    "type": "Deposited",
                    "dp": True,
                    "crumbs": ["Deposit Now", "Depositing", "Deposited"]
                }
            else:
                context = {
                    "depositing": "yes",
                    "price": price,
                    "type": "Depositing",
                    "dp": True,
                    "crumbs": ["Deposit Now", "Depositing"]
                }
        else:
            context = {
                "depositing": "no",
                "type": "Deposit Now",
                "crumbs": ["Deposit Now"]
            }
        return render(request, "auth/deposit.html", context)
    else:
        return redirect("/auth/account/login/")
