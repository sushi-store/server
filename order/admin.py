from django.contrib import admin
from django import forms
from .models import Order, OrderItem
from user.models import Address


@admin.action(description='Set orders status in progress')
def set_in_progress(modeladmin, request, queryset):
    queryset.update(status='I')


@admin.action(description='Set orders status done')
def set_done(modeladmin, request, queryset):
    queryset.update(status='D')


@admin.action(description='Set orders status cancelled')
def set_cancelled(modeladmin, request, queryset):
    queryset.update(status='C')


class AddressInline(admin.StackedInline):
    model = Address
    fields = ('street_name', 'house_number',
              'entrance_number', 'apartments_number')


class OrdersInline(admin.StackedInline):
    model = OrderItem
    verbose_name = "Order Item"
    verbose_name_plural = "Order Items"

    def get_max_num(self, request, obj=None, **kwargs):
        return None

    def get_min_num(self, request, obj=None, **kwargs):
        return 1

    def get_extra(self, request, obj=None, **kwargs):
        return 0


class OrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("customer_name", "email",
                  "phone_number", "delivery_type", "payment_method")


class OrderAdmin(admin.ModelAdmin):
    form = OrderModelForm
    list_filter = ('status',)
    list_display = ('phone_number',
                    'customer_name', 'get_address', 'price', 'status', 'date_of_order')
    inlines = (AddressInline, OrdersInline, )
    actions = [set_in_progress, set_done, set_cancelled]

    @admin.display(description='Order Address')
    def get_address(self, obj):
        return Address.objects.get(order=obj)


admin.site.register(Order, OrderAdmin)
