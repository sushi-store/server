from django.db import models
from sushi.models import Sushi
from phonenumber_field.modelfields import PhoneNumberField


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
    email = models.EmailField(blank=True)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
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

    def save(self, *args, **kwargs):
        # print(self.orderitem_set.all())
        for order_item in self.orderitem_set.all():
            self.price = order_item.sushi.price * order_item.amount
        super(OrderSushi, self).save(*args, **kwargs)


class OrderItem(models.Model):
    sushi = models.ForeignKey(Sushi, on_delete=models.CASCADE)
    order = models.ForeignKey(OrderSushi, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(default=1)

    class Meta:
        unique_together = ('order', 'sushi')
        verbose_name_plural = "Sushi Orders"

    def __str__(self) -> str:
        return f"{self.sushi}: {self.amount}"
