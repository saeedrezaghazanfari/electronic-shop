# Generated by Django 3.1.3 on 2020-11-14 15:02

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Eshop_Product', '0007_auto_20201107_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='timeStamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 14, 15, 2, 27, 585250, tzinfo=utc), verbose_name='زمان ثبت'),
        ),
    ]
