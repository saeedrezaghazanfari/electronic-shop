from django.db import models
from ckeditor.fields import RichTextField
from django.db.models import Q
import os
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.html import format_html
from Extentions.utils import jalali_convertor

class ProductManager(models.Manager):
    def get_by_id(self, product_id):
        return self.get_queryset().get(id=product_id)
    def get_active_products(self):
        return self.get_queryset().filter(active=True)
    def search_category(self, category):
        return self.get_queryset().filter(categories__title__iexact=category, active=True).distinct()
    def search_Brands(self, brand):
        return self.get_queryset().filter(brand__iexact=brand).distinct()
    def search_NameBrandTag(self, field):
        lookup = (
                Q(title__icontains=field, active=True) |
                Q(brand__contains=field, active=True) |
                Q(tag__title__icontains=field, active=True)
        )
        return self.get_queryset().filter(lookup, active=True).distinct()

def get_filename_ext_rand(filepath):
    from random import randint
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    random_id = randint(1000, 9999)
    return name, ext, random_id

def upload_image_path(instance, filename):
    name, ext, rand = get_filename_ext_rand(filename)
    final_name = f"{name}-{rand}{ext}"
    return f"product_img/{final_name}"

def upload_image_path_gallery(instance, filename):
    name, ext, rand = get_filename_ext_rand(filename)
    final_name = f"{name}-{rand}{ext}"
    return f"product_gallery/{final_name}"

class Category(models.Model):
    title = models.CharField(max_length=120, verbose_name='عنوان')
    active = models.BooleanField(default=False, verbose_name='فعال / روح')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.title

    def counter_category_items(self):
        title = self.title
        counter = Product.objects.filter(categories__title__iexact=title, active=True).count()
        return counter

class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name='نام محصول')
    price = models.BigIntegerField(verbose_name='قیمت محصول')
    brand = models.CharField(max_length=100, verbose_name='برند' ,blank=True, null=True)
    image = models.ImageField(upload_to=upload_image_path, verbose_name='تصویر محصول')
    description = RichTextField(verbose_name='توضیحات')
    timeStamp = models.DateTimeField(default=timezone.now(), verbose_name='زمان ثبت')
    categories = models.ManyToManyField(Category, verbose_name='دسته بندی')
    active = models.BooleanField(default=False, verbose_name='نمایش / روح')
    views = models.PositiveIntegerField(default=0, verbose_name='تعداد بازدید')
    is_off = models.BooleanField(default=False, verbose_name='تخفیف دارد:')

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ['-id']

    objects = ProductManager()

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return f'/Product/Details/{self.id}/{self.title.replace(" ","-")}'

    def jimage(self):
        return format_html(f'<img src="{self.image.url}" style="width:100px; height: 60px;">')
    jimage.short_description = 'تصویر محصول'

    def jtimeStamp(self):
        return jalali_convertor(self.timeStamp)
    jtimeStamp.short_description = 'زمان ثبت'

class Tag(models.Model):
    products = models.ManyToManyField(Product, verbose_name='محصولات')
    title = models.CharField(max_length=100, verbose_name='عنوان تگ')
    timeStamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False, verbose_name='فعال / روح')

    class Meta:
        verbose_name = 'تگ'
        verbose_name_plural = 'تگ ها'

    def __str__(self):
        return self.title

class ProductGallery(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    image = models.ImageField(upload_to=upload_image_path_gallery, verbose_name='تصویر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محسول')

    class Meta:
        verbose_name = 'گالری'
        verbose_name_plural = 'گالری محصولات'

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

class ProductVeiw(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول', blank=True, null=True)

    class Meta:
        verbose_name='بازدید محصول'
        verbose_name_plural='بازدید محصولات'

    def __str__(self):
        return f'{self.user} - {self.product}'

class Favorites(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')

    class Meta:
        verbose_name='علاقه مندی'
        verbose_name_plural='علاقه مندی ها'

    def __str__(self):
        return f'{self.user} - {self.product}'

class ProductBrand(models.Model):
    productId =  models.PositiveIntegerField(default=0, verbose_name='آیدی محصول', blank=True, null=True)
    productName = models.CharField(max_length=225, verbose_name='نام محصول', blank=True, null=True)
    productBrand = models.CharField(max_length=225, verbose_name='برند محصول', blank=True, null=True)

    class Meta:
        verbose_name='برند محصول'
        verbose_name_plural='برند های محصولات'

    def __str__(self):
        return f'{self.productId} - {self.productName} - {self.productBrand}'

class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='کالا')
    color = models.CharField(max_length=120, verbose_name='رنگ کالا')
    active = models.BooleanField(default=False, verbose_name='نمایش / روح')

    class Meta:
        verbose_name='رنگ محصول'
        verbose_name_plural='رنگ محصولات'

    def __str__(self):
        return f'{self.product} - {self.color}'

class Chart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='chartproduct', verbose_name='محصول')
    price = models.PositiveIntegerField(default=0, verbose_name='قیمت')
    timeStamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='نمودار محصول'
        verbose_name_plural='نمودار محصولات'

    def __str__(self):
        return f'{self.product} - {self.price} - {self.timeStamp}'

