from django.shortcuts import render

from creyp.utils import send_contact_us_email

# Error Code Page Views
def error_404_view(request, exception):
    return render(request, "pages/errors/404.html")
def index(request):
    return render(request, "pages/index.html")


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
