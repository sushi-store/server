from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from sushi.models import Sushi
import logging


class OrderSushi(models.Model):
    ORDER_STATUS = (
        ('P', 'Pending'),
        ('I', 'In Process'),
        ('D', 'Done'),
        ('C', 'Cancelled'),
    )
    DELIVERIES_TYPES = (
        ('P', 'Pickup'),
        ('D', 'Delivery'),
    )
    PAYMENT_METHODS = (
        ('C', 'Cash'),
        ('D', 'Card'),
    )
    customer_name = models.CharField(max_length=50)
    customer_last_name = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    phone_number = PhoneNumberField(null=False, blank=False)
    delivery_type = models.CharField(
        max_length=1, default='D', choices=DELIVERIES_TYPES)
    payment_method = models.CharField(
        max_length=1, default='С', choices=PAYMENT_METHODS)
    status = models.CharField(max_length=1, default='P', choices=ORDER_STATUS)
    price = models.PositiveIntegerField(default=0)
    date_of_order = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Orders"

    def __str__(self) -> str:
        return f"Order #{self.id}"


@receiver(pre_save, sender=OrderSushi)
def update_price(sender, instance, **kwargs):
    instance.price = 0
    for order_item in instance.orderitem_set.all():
        instance.price += order_item.sushi.price * order_item.amount


class OrderItem(models.Model):
    sushi = models.ForeignKey(Sushi, on_delete=models.CASCADE)
    order = models.ForeignKey(OrderSushi, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(default=1)

    class Meta:
        unique_together = ('order', 'sushi')
        verbose_name_plural = "Sushi Orders"

    def __str__(self) -> str:
        return f"{self.sushi}: {self.amount}"
