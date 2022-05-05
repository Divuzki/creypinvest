import os
from django.conf import settings
import string
import random
from django.core.mail import send_mail
import threading
from django.utils.html import strip_tags
from django.template.loader import render_to_string

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADMIN_EMAIL = settings.EMAIL_HOST_USER


def truncate_string(value, max_length=45, suffix="skt"):
    string_value = str(value)
    string_truncated = string_value[:min(
        len(string_value), (max_length - len(suffix)))]
    suffix = (suffix if len(string_value) > max_length else '')
    return suffix+string_truncated


def random_string_generator(size=50, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# ROT13 ENCRYPTION
rot13trans = str.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
                           'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm')


# Function to translate plain text
def rot13_encrypt(text):
    return text.translate(rot13trans)
# Account Section
class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def send_contact_us_email(request, name=None, phone=None, user_email=None, subject=None, body=None, toAdmin=False):
    email_subject = subject
    email_body = render_to_string('account/email/contact_us_email_sent.html', {
        'email_subject': email_subject,
        'email': user_email,
        'name': name,
        'phone': phone,
        'body': body,
        'toAdmin': toAdmin
    }, request)
    text_content = strip_tags(email_subject)
    if toAdmin == True:
        email = send_mail(
            email_subject, text_content, ADMIN_EMAIL, [ADMIN_EMAIL], html_message=email_body)
    else:
        email = send_mail(
            email_subject, text_content, ADMIN_EMAIL, [user_email], html_message=email_body)

    if not settings.DEBUG:
        EmailThread(email).start()
