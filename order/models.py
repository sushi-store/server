from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from sushi.models import Sushi


class Order(models.Model):
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
    customer_name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone_number = PhoneNumberField(null=False, blank=False)
    delivery_type = models.CharField(
        max_length=1, default='D', choices=DELIVERIES_TYPES)
    payment_method = models.CharField(
        max_length=1, default='С', choices=PAYMENT_METHODS)
    user_id = models.PositiveIntegerField(null=True, default=None)
    uuid = models.CharField(max_length=50, null=True, default=None)
    status = models.CharField(max_length=1, default='P', choices=ORDER_STATUS)
    date_of_order = models.DateTimeField(auto_now=True)

    @property
    def price(self):
        full_price = 0
        for order_item in self.order.all():
            full_price += order_item.sushi.price * order_item.amount
        return full_price

    @property
    def amount(self):
        total_amount = 0
        for order_item in self.order.all():
            total_amount += order_item.amount
        return total_amount

    class Meta:
        verbose_name_plural = "Orders"

    def __str__(self) -> str:
        return f"Order #{self.id}"


class OrderItem(models.Model):
    sushi = models.ForeignKey(
        Sushi, on_delete=models.CASCADE, related_name='sushi')
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order')
    amount = models.PositiveSmallIntegerField(default=1)

    class Meta:
        unique_together = ('order', 'sushi')
        verbose_name_plural = "Sushi Orders"

    def __str__(self) -> str:
        return f"{self.sushi}: {self.amount}"
