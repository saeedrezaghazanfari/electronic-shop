# Generated by Django 3.1.3 on 2020-11-06 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eshop_Product', '0003_auto_20201106_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='timeStamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
