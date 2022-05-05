from django.contrib import admin

from users.models import Profile, Wallet, Transaction, AdminWallet

admin.site.register(Profile)
admin.site.register(Wallet)
admin.site.register(AdminWallet)
admin.site.register(Transaction)
