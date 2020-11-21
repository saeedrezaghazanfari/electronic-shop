from django.contrib.auth.models import User

from django.db import models
from ckeditor.fields import RichTextField

def get_filename_ext_rand(filepath):
    import os
    from random import randint
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    random_id = randint(1000, 9999)
    return name, ext, random_id

def upload_image_path(instance, filename):
    name, ext, rand = get_filename_ext_rand(filename)
    final_name = f"{name}-{rand}{ext}"
    return f"slider_img/{final_name}"

def upload_image_path_brand(instance, filename):
    name, ext, rand = get_filename_ext_rand(filename)
    final_name = f"{name}-{rand}{ext}"
    return f"brand_img/{final_name}"

class MainSlider(models.Model):
    image = models.ImageField(upload_to=upload_image_path, verbose_name='تصویر')
    url = models.URLField(verbose_name='لینک')
    message = models.CharField(max_length=200, verbose_name='پیام')
    active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'اسلاید'
        verbose_name_plural = 'اسلاید ها'

    def __str__(self):
        return self.message

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

class Brands(models.Model):
    title = models.CharField(max_length=100, verbose_name='نام برند')
    image = models.ImageField(upload_to=upload_image_path_brand, verbose_name='برند')
    url = models.URLField(blank=True, null=True, verbose_name='لینک')
    active = models.BooleanField(default=False, verbose_name='نمایش / روح')

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند ها'

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title

class Notification(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    notification = RichTextField(verbose_name='متن اعلان')
    url = models.URLField(verbose_name='لینک مربوطه', blank=True, null=True)
    active = models.BooleanField(default=False, verbose_name='فعال / روح')

    class Meta:
        verbose_name = 'اعلان'
        verbose_name_plural = 'اعلانات'

    def __str__(self):
        return self.title

class Send_Notifications_email_Model(models.Model):
    user = models.ForeignKey(User, verbose_name='کاربر', on_delete=models.CASCADE)
    activeSend = models.BooleanField(default=True, verbose_name='ارسال ایمیل')

    class Meta:
        verbose_name='ایمیل اعلان'
        verbose_name_plural='ایمیل اعلانات'

    def __str__(self):
        return f'{self.user}-{self.activeSend}'

class Emails(models.Model):
    subject = models.CharField(max_length=225, verbose_name='عنوان')
    content = models.TextField(verbose_name='محتوای ایمیل')
    timeStamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='ایمیل'
        verbose_name_plural='ایمیل ها'

    def __str__(self):
        return f'{self.subject} - {self.timeStamp}'