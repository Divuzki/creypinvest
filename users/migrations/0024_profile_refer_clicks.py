# Generated by Django 4.0.4 on 2022-05-09 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_profile_referred_by_profile_refers'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='refer_clicks',
            field=models.IntegerField(default=0),
        ),
    ]
