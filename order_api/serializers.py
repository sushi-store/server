from user.models import Address
from rest_framework import serializers
from order.models import Order, OrderItem
from sushi_api.serializers import SushiSerializer
from user_api.serializers import AddressSerializer
from sushi.models import Sushi
from rest_framework.exceptions import NotAcceptable
from phonenumber_field.serializerfields import PhoneNumberField


class DeliveryTypeSerializer(serializers.Field):

    DELIVERIES_TYPES = {
        'P': {'en': 'Pickup', 'uk': 'Самовивіз'},
        'D': {'en': 'Delivery', 'uk': 'Доставка'},
    }

    def to_representation(self, obj):
        return self.DELIVERIES_TYPES[obj]

    def to_internal_value(self, data):
        for item in self.DELIVERIES_TYPES:
            if data in list(self.DELIVERIES_TYPES[item].values()):
                return item


class PaymentMethodSerializer(serializers.Field):

    PAYMENT_METHODS = {
        'C': {'en': 'Cash', 'uk': 'Готівкою'},
        'D': {'en': 'Card', 'uk': 'Картою'}
    }

    def to_representation(self, obj):
        return self.PAYMENT_METHODS[obj]

    def to_internal_value(self, data):
        for item in self.PAYMENT_METHODS:
            if data in list(self.PAYMENT_METHODS[item].values()):
                return item


class StatusSerializer(serializers.Field):

    ORDER_STATUS = {
        'P': {'en': 'Pending', 'uk': 'В обробці'},
        'I': {'en': 'In Process', 'uk': 'Виконується'},
        'D': {'en': 'Done', 'uk': 'Готовий'},
        'C': {'en': 'Cancelled', 'uk': 'Скасований'}
    }

    def to_representation(self, obj):
        return self.ORDER_STATUS[obj]

    def to_internal_value(self, data):
        for item in self.ORDER_STATUS:
            if data in list(self.ORDER_STATUS[item].values()):
                return item


class OrderItemSerializer(serializers.ModelSerializer):
    slug = serializers.CharField()

    class Meta:
        model = OrderItem
        fields = ['slug', 'amount']

    def create(self, validated_data):
        instance = self.Meta.model(sushi=Sushi.objects.get(
            slug=validated_data.get('slug')), **validated_data)
        instance.save()
        return instance

    def to_representation(self, instance):
        data = SushiSerializer(instance=instance.sushi, context={
                               'request': self.context.get('request')}).data
        data['amount'] = instance.amount
        return data


class OrderSerializer(serializers.ModelSerializer):
    customerName = serializers.CharField(source='customer_name')
    userId = serializers.IntegerField(source='user_id', allow_null=True)
    phoneNumber = PhoneNumberField(source='phone_number')
    dateOfOrder = serializers.DateTimeField(
        source='date_of_order', format="%d-%m-%Y %H:%M:%S", read_only=True)
    deliveryType = DeliveryTypeSerializer(source='delivery_type')
    paymentMethod = PaymentMethodSerializer(source='payment_method')
    status = StatusSerializer(read_only=True)
    address = AddressSerializer(source='order_address')
    order = OrderItemSerializer(many=True)
    price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'userId', 'uuid', 'customerName',
                  'email', 'phoneNumber', 'deliveryType', 'paymentMethod',  'address', 'order', 'price', 'amount', 'status', 'dateOfOrder']

    def create(self, validated_data):
        try:
            order_items = validated_data.pop('order')
        except KeyError as error:
            raise NotAcceptable(error)
        try:
            address = validated_data.pop('order_address')
            if not (validated_data.get('delivery_type') == 'D' and address['street_name'] and address['house_number']) and not validated_data.get('delivery_type') == 'P':
                raise NotAcceptable('Deliverty type should have address.')
        except KeyError as error:
            raise NotAcceptable(error)
        instance = self.Meta.model(**validated_data)
        instance.save()
        for order_item in order_items:
            OrderItem.objects.create(order=instance, sushi=Sushi.objects.get(
                slug=order_item['slug']), amount=order_item['amount'])
        Address.objects.create(order=instance, **address)
        return instance

    def get_price(self, obj):
        return obj.price

    def get_amount(self, obj):
        return obj.amount
