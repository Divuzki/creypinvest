# Generated by Django 4.0.4 on 2022-05-07 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_profile_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='msg',
            field=models.TextField(blank=True),
        ),
    ]
