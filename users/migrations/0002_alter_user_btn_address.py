# Generated by Django 4.0.2 on 2022-02-05 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='btn_address',
            field=models.CharField(max_length=40, unique=True),
        ),
    ]
