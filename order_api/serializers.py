from user.models import Address
from rest_framework import serializers
from order.models import Order, OrderItem
from sushi_api.serializers import SushiSerializer
from user_api.serializers import AddressSerializer
from sushi.models import Sushi
from rest_framework.exceptions import NotAcceptable
from phonenumber_field.serializerfields import PhoneNumberField
import logging


class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)


class OrderItemSerializer(serializers.ModelSerializer):
    sushi = SushiSerializer()

    class Meta:
        model = OrderItem
        fields = ['sushi', 'amount']


class OrderSerializer(serializers.ModelSerializer):
    customerName = serializers.CharField(source='customer_name')
    customerLastName = serializers.CharField(source='customer_last_name')
    phoneNumber = PhoneNumberField(source='phone_number')
    dateOfOrder = serializers.DateTimeField(
        source='date_of_order', read_only=True)
    deliveryType = ChoiceField(
        source='delivery_type', choices=Order.DELIVERIES_TYPES)
    paymentMethod = ChoiceField(
        source='payment_method', choices=Order.PAYMENT_METHODS)
    status = serializers.SerializerMethodField(
        'get_status', read_only=True)
    address = AddressSerializer(source='order_address')
    orderItems = OrderItemSerializer(source='order', many=True)
    price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customerName', 'customerLastName',
                  'email', 'phoneNumber', 'deliveryType', 'paymentMethod', 'status', 'address', 'orderItems', 'price', 'dateOfOrder']

    def create(self, validated_data):
        logger = logging.getLogger('logger')
        logger.info(validated_data)
        try:
            order_items = validated_data.pop('order')
        except KeyError as error:
            raise NotAcceptable(error)
        try:
            address = validated_data.pop('order_address')
        except KeyError as error:
            raise NotAcceptable(error)
        instance = self.Meta.model(**validated_data)
        instance.save()
        for order_item in order_items:
            sushi = order_item.pop('sushi')
            OrderItem.objects.create(order=instance, sushi=Sushi.objects.get(
                slug=sushi['slug']), **order_item)
        Address.objects.create(order=instance, **address)
        return instance

    def get_price(self, obj):
        return obj.price

    def get_status(self, obj):
        return obj.get_status_display()
