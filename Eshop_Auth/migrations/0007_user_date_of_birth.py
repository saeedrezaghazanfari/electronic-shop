# Generated by Django 3.1.3 on 2020-11-07 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eshop_Auth', '0006_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]