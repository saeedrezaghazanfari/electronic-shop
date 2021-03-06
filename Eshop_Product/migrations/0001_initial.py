# Generated by Django 3.1.3 on 2020-11-02 09:29

import Eshop_Product.models
import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='عنوان')),
                ('active', models.BooleanField(default=False, verbose_name='فعال / روح')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='نام محصول')),
                ('price', models.BigIntegerField(verbose_name='قیمت محصول')),
                ('brand', models.CharField(blank=True, max_length=100, null=True, verbose_name='برند')),
                ('image', models.ImageField(upload_to=Eshop_Product.models.upload_image_path, verbose_name='تصویر محصول')),
                ('description', ckeditor.fields.RichTextField(verbose_name='توضیحات')),
                ('timeStamp', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False, verbose_name='نمایش / روح')),
                ('views', models.PositiveIntegerField(default=0, verbose_name='تعداد بازدید')),
                ('categories', models.ManyToManyField(to='Eshop_Product.Category', verbose_name='دسته بندی')),
            ],
            options={
                'verbose_name': 'محصول',
                'verbose_name_plural': 'محصولات',
            },
        ),
        migrations.CreateModel(
            name='ProductBrand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productId', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='آیدی محصول')),
                ('productName', models.CharField(blank=True, max_length=225, null=True, verbose_name='نام محصول')),
                ('productBrand', models.CharField(blank=True, max_length=225, null=True, verbose_name='برند محصول')),
            ],
            options={
                'verbose_name': 'برند محصول',
                'verbose_name_plural': 'برند های محصولات',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان تگ')),
                ('timeStamp', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False, verbose_name='فعال / روح')),
                ('products', models.ManyToManyField(to='Eshop_Product.Product', verbose_name='محصولات')),
            ],
            options={
                'verbose_name': 'تگ',
                'verbose_name_plural': 'تگ ها',
            },
        ),
        migrations.CreateModel(
            name='ProductVeiw',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Eshop_Product.product', verbose_name='محصول')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'بازدید محصول',
                'verbose_name_plural': 'بازدید محصولات',
            },
        ),
        migrations.CreateModel(
            name='ProductGallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان')),
                ('image', models.ImageField(upload_to=Eshop_Product.models.upload_image_path_gallery, verbose_name='تصویر')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Eshop_Product.product', verbose_name='محسول')),
            ],
            options={
                'verbose_name': 'گالری',
                'verbose_name_plural': 'گالری محصولات',
            },
        ),
        migrations.CreateModel(
            name='ProductColor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=120, verbose_name='رنگ کالا')),
                ('active', models.BooleanField(default=False, verbose_name='نمایش / روح')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Eshop_Product.product', verbose_name='کالا')),
            ],
            options={
                'verbose_name': 'رنگ محصول',
                'verbose_name_plural': 'رنگ محصولات',
            },
        ),
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Eshop_Product.product', verbose_name='محصول')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'علاقه مندی',
                'verbose_name_plural': 'علاقه مندی ها',
            },
        ),
    ]
