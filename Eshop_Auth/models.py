
# from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
import os

# class User(AbstractUser):
    # ip = ....
    # avator = models.ImageField(upload_to=upload_image_path_profile, default='/img/eshop.png', verbose_name='تصویر پروفایل')
    # phone = models.PositiveBigIntegerField(verbose_name='شماره تماس', blank=True, null=True, default=0)
    # webName = models.CharField(max_length=100, verbose_name='آدرس وبسایت', blank=True, null=True)
    # bio = models.TextField(verbose_name='بیوگرافی', blank=True, null=True)
    # def delete(self, *args, **kwargs):
    #     self.avatar.delete()
    #     super().delete(*args, **kwargs)

def get_filename_ext_rand(filepath):
    from random import randint
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    random_id = randint(1000, 9999)
    return name, ext, random_id

def upload_image_path_profile(instance, filename):
    name, ext, rand = get_filename_ext_rand(filename)
    final_name = f"{name}-{rand}{ext}"
    return f"profile-image/{final_name}"

def upload_image_path_ImageErrSpam(instance, filename):
    name, ext, rand = get_filename_ext_rand(filename)
    final_name = f"{name}-{rand}{ext}"
    return f"Image_Report_Spam/{final_name}"

class UltraProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='مالک پروفایل')
    avator = models.ImageField(upload_to=upload_image_path_profile, default='/img/eshop.png', verbose_name='تصویر پروفایل')
    phone = models.PositiveBigIntegerField(verbose_name='شماره تماس', blank=True, null=True, default=0)
    webName = models.CharField(max_length=100, verbose_name='آدرس وبسایت', blank=True, null=True)
    bio = models.TextField(verbose_name='بیوگرافی', blank=True, null=True)

    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل ها'

    def delete(self, *args, **kwargs):
        self.avator.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.user.username

class ReportSpam_Model(models.Model):
    username = models.CharField(max_length=100, verbose_name='نام کاربری')
    email = models.EmailField(max_length=255, verbose_name='ایمیل')
    imageErr = models.ImageField(upload_to=upload_image_path_ImageErrSpam, verbose_name='تصویر خطا')
    subject = models.CharField(max_length=100, verbose_name='عنوان خطا')
    msg = models.TextField(verbose_name='متن پیام')

    class Meta:
        verbose_name = 'گزارش خطا'
        verbose_name_plural = 'گزارش خطاها'

    def delete(self, *args, **kwargs):
        self.imageErr.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f'{self.username} - {self.subject}'