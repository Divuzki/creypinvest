# Generated by Django 4.0.4 on 2022-05-07 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_alter_wallet_btn_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='profile-image-placeholder.png', upload_to='profile-image/%h/%Y/'),
        ),
    ]
