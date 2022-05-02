from django.contrib import admin

from users.models import Profile, Wallet, Transactions

admin.site.register(Profile)
admin.site.register(Wallet)
admin.site.register(Transactions)
