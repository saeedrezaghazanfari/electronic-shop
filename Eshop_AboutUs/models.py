from django.db import models
from ckeditor.fields import RichTextField

def get_filename_ext_rand(filepath):
    import os
    from random import randint
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    random_id = randint(1000, 9999)
    return name, ext, random_id

def upload_image_path_LoGo(instance, filename):
    name, ext, rand = get_filename_ext_rand(filename)
    final_name = f"{name}-{rand}{ext}"
    return f"Web_Logo/{final_name}"

class SiteSetting(models.Model):
    App_Name = models.CharField(max_length=100, verbose_name='نام فروشگاه', blank=True, null=True)
    Logo = models.ImageField(upload_to=upload_image_path_LoGo, verbose_name='لوگوی وبسایت', blank=True, null=True)
    Email = models.CharField(max_length=200, verbose_name='ایمیل')
    fax = models.IntegerField(verbose_name='فکس')
    Telegram = models.CharField(max_length=100, verbose_name='تلگرام')
    Whatsup = models.BigIntegerField(verbose_name='شماره ی واتس آپ')
    Youtube = models.CharField(max_length=100, verbose_name='یوتیوب')
    Instagram = models.CharField(max_length=100, verbose_name='اینستاگرام')
    Phone_Number = models.BigIntegerField(verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')
    AboutUs = RichTextField(verbose_name='توضیحاتی درباره ی سایت')
    X_inTheWorld = models.FloatField(verbose_name='مختصات X در نقشه', default=0, blank=True, null=True)
    Y_inTheWorld = models.FloatField(verbose_name='مختصات Y در نقشه', default=0, blank=True, null=True)

    class Meta:
        verbose_name = 'درباره ی ما'
        verbose_name_plural = 'تنظیمات درباره ی ما'

    def __str__(self):
        return self.Email