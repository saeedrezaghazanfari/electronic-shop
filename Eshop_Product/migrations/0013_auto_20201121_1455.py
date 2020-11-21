# Generated by Django 3.1.3 on 2020-11-21 11:25

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Eshop_Product', '0012_auto_20201115_0016'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_off',
            field=models.BooleanField(default=False, verbose_name='تخفیف دارد:'),
        ),
        migrations.AlterField(
            model_name='product',
            name='timeStamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 21, 11, 25, 0, 957086, tzinfo=utc), verbose_name='زمان ثبت'),
        ),
    ]
