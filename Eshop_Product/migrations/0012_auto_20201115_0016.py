# Generated by Django 3.1.3 on 2020-11-14 20:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Eshop_Product', '0011_auto_20201115_0016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='timeStamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 14, 20, 46, 43, 565405, tzinfo=utc), verbose_name='زمان ثبت'),
        ),
    ]
