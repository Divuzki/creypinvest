from multiprocessing import context
from django.shortcuts import redirect, render

from creyp.utils import send_contact_us_email, set_cookie_function

# Error Code Page Views


def error_404_view(request, exception):
    return render(request, "pages/errors/404.html")


def index(request):
    return render(request, "pages/index.html")


def referral_view(request, username):
    cookie = request.COOKIES.get("_refered_by", None) == None
    user = request.user
    is_user = str(request.user.username) == str(username)
    context = {}
    if not user.is_authenticated:
        if cookie == True:
            context = {
                "username": username,
                "title": "Congratulation",
                "message": f"You have been referred by {username}, now signup and get your $100 welcoming gift! when you deposit above $1,000",
                "btn": "signup"
            }
            res = render(request, "pages/referral.html", context)
            set_cookie_function("_refered_by", str(username),
                                max_age=500*1900, response=res)
        else:
            context = {
                "username": username,
                "title": "Hey!",
                "message": "You were already been referred, just login deposit above $1,000 and get your $100 welcoming gift!",
                "btn": "signup"
            }
            res = render(request, "pages/referral.html", context)
    elif user.is_authenticated:
        if is_user:
            context = {
                "username": username,
                "title": f"Sorry {user.username}",
                "message": "You can not refer yourself",
                "btn": "back"
            }
            res = render(request, "pages/referral.html", context)
        else:
            return redirect("dashboard-home")
    return res


def about(request):
    return render(request, "pages/about.html", {"type": "About CreypInvest Inc.", "crumbs": ["About Us"]})


def contact(request):
    return render(request, "pages/contact.html", {"type": "Contact Support Team At CreypInvest Inc.", "crumbs": ["Contact Us"]})


def send_contact_email(request):
    res = render(request, "pages/message_page.html",
                 {"title": "Oops", "msg": "Sorry, something is wrong with the server but you can mail us at <a href='mailto:creypinvest@gmail.com'>creypinvest@gmail.com</a>"})
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        body = request.POST.get("message")
        try:
            send_contact_us_email(request, name, phone,
                                  email, subject, body, toAdmin=True)
            send_contact_us_email(request, name, phone, email, "Email Recieved!",
                                  "Your Email Has Been Received, We Will Get Back To You A Soon As Possible")
            res = render(request, "pages/message_page.html",
                         {"title": "Yay!", "msg": "Your mail has been sent to us"})
        except:
            res = render(request, "pages/message_page.html", {
                         "title": "Oops", "msg": "Sorry, something is wrong with the server but you can mail us at <a href='mailto:creypinvest@gmail.com'>creypinvest@gmail.com</a>"})
    return res
