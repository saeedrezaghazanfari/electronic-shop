# Generated by Django 3.1.3 on 2020-11-21 18:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Eshop_Product', '0013_auto_20201121_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='timeStamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 21, 18, 13, 41, 105019, tzinfo=utc), verbose_name='زمان ثبت'),
        ),
    ]
