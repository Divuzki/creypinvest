# Generated by Django 4.0.4 on 2022-05-05 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_rename_transactions_transaction_adminwallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminwallet',
            name='btn_address',
            field=models.TextField(unique=True),
        ),
    ]
