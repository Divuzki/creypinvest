# Generated by Django 4.0.4 on 2022-05-07 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_transaction_msg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transactionId',
            field=models.CharField(max_length=17),
        ),
    ]
