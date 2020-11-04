from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

class ContactModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام کاربر')
    email = models.EmailField(verbose_name='ایمیل کاربر')
    subject = models.CharField(max_length=100, verbose_name='عنوان پیام')
    msg = RichTextField(verbose_name='متن پیام کاربر')
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name = 'پیام کاربران'
        verbose_name_plural = 'پیام های کاربران'

    def __str__(self):
        return self.name

class OpinionModel(models.Model):
    username = models.CharField(max_length=100, verbose_name='نام کاربری', blank=True, null=True)
    opinion = RichTextUploadingField(verbose_name='نظر / انتقاد / پیشنهاد کاربر')
    timeStamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'نظر / انتقاد / پیشنهاد'
        verbose_name_plural = 'نظرات / انتقادات / پیشنهادات'

    def __str__(self):
        return self.username