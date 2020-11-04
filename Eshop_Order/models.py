from django.contrib.auth.models import User
from django.db import models

from Eshop_Product.models import Product


class Order(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=0,verbose_name='مالک سبد خرید')
    is_paid = models.BooleanField(default=False, verbose_name='تسویه')
    paymentDate = models.DateTimeField(blank=True, null=True, verbose_name='تاریخ پرداخت')
    ref_Id = models.PositiveBigIntegerField(blank=True, null=True, verbose_name='کد پیگیری')

    class Meta:
        verbose_name='سبد خرید'
        verbose_name_plural='سبد های خرید'

    def __str__(self):
        return self.owner.username

    def get_final_total(self):
        amount = 0
        for i in self.orderdetails_set.all():
            amount += i.price * i.count
        return amount

    def get_ref_id(self):
        from random import randint
        import datetime
        randNum = randint(10000, 99999)
        x = datetime.datetime.now()
        day = x.strftime("%d")
        month = x.strftime("%m")
        year = x.strftime("%Y")
        refId = f'{randNum}-{year}-{month}-{day}'
        return refId


class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=0, verbose_name='سبد خرید')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=0, verbose_name='محصول')
    count = models.PositiveIntegerField(default=0, verbose_name='تعداد محصول')
    price = models.PositiveBigIntegerField(default=0, verbose_name='قیمت محصول')
    productColor = models.CharField(max_length=120, blank=True, null=True, verbose_name='رنگ محصول')

    class Meta:
        verbose_name = 'جزئیات سبد خرید'
        verbose_name_plural = 'جزئیات سبد های خرید'

    def __str__(self):
        return f'{self.order.owner} - {self.product.title}'

    def get_priceCount_total(self):
        total = self.price * self.count
        return total

class OffCode(models.Model):
    offcode = models.CharField(max_length=225, blank=True, null=True, verbose_name='کد تخفیف')
    many = models.PositiveIntegerField(default=0, verbose_name='درصد تخفیف')
    active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'کد تخفیف'
        verbose_name_plural = 'کدهای تخفیف'

    def __str__(self):
        return f'{self.offcode} - {self.active}'