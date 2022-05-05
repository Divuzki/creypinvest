from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


STATUS = (
    ("pending", "pending"),
    ("processing", "processing"),
    ("confirming", "confirming"),
    ("processed", "processed"),
    ("error", "error"),
    ("server error", "server error")
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    signup_confirmation = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Wallet(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    btn_address = models.CharField(max_length=40, unique=True)
    bonus = models.CharField(max_length=4)
    balance = models.CharField(max_length=10)
    pin = models.CharField(max_length=4)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.btn_address} | bal : {self.balance}"


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.CharField(max_length=10)
    status = models.CharField(max_length=15, choices=STATUS)
    transactionId = models.IntegerField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"user has {self.wallet.balance} | TID: {self.transactionID}"
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