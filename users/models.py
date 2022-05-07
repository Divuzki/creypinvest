from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from creyp.utils import random_string_generator

from PIL import Image
from django_countries.fields import CountryField


STATUS = (
    ("pending", "pending"),
    ("credit", "credit"),
    ("processing", "processing"),
    ("confirming", "confirming"),
    ("processed", "processed"),
    ("error", "error"),
    ("server error", "server error")
)
GENDER = (
    ("female", "female"),
    ("male", "male"),
    ("other", "other")
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to="profile-image/%h/%Y/",
                              default="profile-image-placeholder.png")
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150, blank=True)
    gender = models.CharField(max_length=15, choices=GENDER, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    country = CountryField(blank=True)
    signup_confirmation = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.image:
            super().save(*args, **kwargs)
            img = Image.open(self.image.path)
            if img.height > 200 or img.width > 200:
                output_size = (200, 200)
                img.thumbnail(output_size)
                img.save(self.image.path)


class Wallet(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    btn_address = models.CharField(max_length=40, blank=True, null=True)
    bonus = models.CharField(max_length=4, default="0", blank=True)
    balance = models.CharField(max_length=10, default="00.00", blank=True)
    pin = models.CharField(max_length=6, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.btn_address} - bal : {self.balance}"


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.CharField(max_length=10, blank=True)
    status = models.CharField(max_length=15, choices=STATUS)
    msg = models.TextField(blank=True)
    transactionId = models.CharField(max_length=17, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"user has {self.wallet.balance} | TID: {self.transactionId}"

    def save(self, *args, **kwargs):
        self.transactionId = random_string_generator(size=17)
        super().save(*args, **kwargs)

class AdminWallet(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    btn_address = models.TextField(unique=True)

    def __str__(self):
        return f"{self.btn_address}"


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


@receiver(post_save, sender=Profile)
def update_wallet_signal(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)
