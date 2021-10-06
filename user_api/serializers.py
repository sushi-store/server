from rest_framework import serializers
from rest_framework.exceptions import NotAcceptable, ParseError
from user.models import CustomerUser, Address
from phonenumber_field.serializerfields import PhoneNumberField
import logging


class TooMuchAddressesError(Exception):
    def __init__(self, message='Too much addresses. Addresses number cannot exceed 3.'):
        super().__init__(message)


class AddressSerializer(serializers.ModelSerializer):
    streetName = serializers.CharField(
        source='street_name', allow_blank=True, allow_null=True, default='')
    houseNumber = serializers.CharField(
        source='house_number', allow_blank=True, allow_null=True, default='')
    entranceNumber = serializers.CharField(
        source='entrance_number', allow_blank=True, allow_null=True, default='')
    apartmentsNumber = serializers.CharField(
        source='apartments_number', allow_blank=True, allow_null=True, default='')

    class Meta:
        model = Address
        fields = ['streetName', 'houseNumber',
                  'entranceNumber', 'apartmentsNumber']


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    addresses = AddressSerializer(many=True, required=False)
    phoneNumber = PhoneNumberField(source='phone_number')
    isEmailConfirmed = serializers.BooleanField(
        read_only=True, source='is_email_confirmed')
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = CustomerUser
        fields = ['email', 'name',
                  'phoneNumber', 'isEmailConfirmed', 'addresses']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['addresses'] = AddressSerializer(
            instance=Address.objects.filter(user=instance), many=True).data
        return data

    def update(self, instance, validated_data):
        addresses = validated_data.get(
            "addresses", {})
        try:
            if len(addresses) <= 3:
                if addresses:
                    Address.objects.filter(user=instance).delete()
                    for address in addresses:
                        Address.objects.create(user=instance, **address)
                return super(UserSerializer, self).update(instance, validated_data)
            else:
                raise TooMuchAddressesError
        except TooMuchAddressesError as e:
            error = {'message': str(e)}
            raise NotAcceptable(error)

    def validate_phoneNumber(self, value):
        users = CustomerUser.objects.exclude(pk=self.instance.pk)
        if users.filter(phone_number__iexact=value).exists():
            raise serializers.ValidationError("Phone number already exists.")
        return value


class RegisterUserSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    addresses = AddressSerializer(many=True, required=False)
    phoneNumber = PhoneNumberField(source='phone_number')
    email = serializers.EmailField()

    class Meta:
        model = CustomerUser
        fields = ['email', 'name',
                  'phoneNumber', 'password', 'addresses']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        try:
            addresses = validated_data.pop('addresses')
        except KeyError:
            addresses = []
        try:
            if len(addresses) <= 3:
                password = validated_data.pop('password', None)
                instance = self.Meta.model(**validated_data)
                instance.is_email_confirmed = False
                if password is not None:
                    instance.set_password(password)
                for address in addresses:
                    Address.objects.create(user=instance, **address)
            else:
                raise Exception('To many addresses included.')
        except TooMuchAddressesError as e:
            error = {'message': str(e)}
            raise NotAcceptable(error)
        instance.save()
        return instance

    def validate_email(self, value):
        lower_email = value.lower()
        if CustomerUser.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError("Email already exists.")
        return lower_email

    def validate_phoneNumber(self, value):
        if CustomerUser.objects.filter(phone_number__iexact=value).exists():
            raise serializers.ValidationError("Phone number already exists.")
        return value
