# Generated by Django 3.1.3 on 2020-11-06 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eshop_Product', '0002_chart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='timeStamp',
            field=models.DateTimeField(),
        ),
    ]
