# Generated by Django 3.1.3 on 2020-11-07 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Eshop_Auth', '0007_user_date_of_birth'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
