# Generated by Django 4.0.4 on 2022-05-07 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_transaction_amount_alter_transaction_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='balance',
            field=models.CharField(blank=True, default='00.00', max_length=10),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='bonus',
            field=models.CharField(blank=True, default='0', max_length=4),
        ),
    ]