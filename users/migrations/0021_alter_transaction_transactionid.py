# Generated by Django 4.0.4 on 2022-05-07 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_alter_transaction_transactionid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transactionId',
            field=models.CharField(blank=True, max_length=17),
        ),
    ]