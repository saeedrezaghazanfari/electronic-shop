# Generated by Django 3.1.3 on 2020-11-05 19:52

import Eshop_Auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eshop_Auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ultraprofile',
            name='avator',
            field=models.ImageField(default='img/eshop.png', upload_to=Eshop_Auth.models.upload_image_path_profile, verbose_name='تصویر پروفایل'),
        ),
    ]
