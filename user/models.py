from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.deletion import CASCADE
from phonenumber_field.modelfields import PhoneNumberField
from order.models import Order


class AccountManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, phone_number, password, **other_fields):

        if not email:
            raise ValueError('You must provide an email address.')

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name,
                          phone_number=phone_number, **other_fields)
        user.set_password(password)
        user.save()
        pass

    def create_superuser(self, email, first_name, last_name, phone_number, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.'
            )
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.'
            )

        return self.create_user(email, first_name, last_name, phone_number, password, **other_fields)


class CustomerUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, blank=True)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    start_date = models.DateTimeField(auto_now=True)

    is_email_confirmed = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['phone_number',
                       'first_name', 'last_name', 'phone_number']

    def __str__(self) -> str:
        return f'{self.last_name} {self.first_name} {self.patronymic}'

    class Meta:
        verbose_name_plural = "Users"


class Address(models.Model):

    street_name = models.CharField(max_length=50)
    street_number = models.CharField(max_length=10)
    entrance_number = models.CharField(max_length=10, blank=True, null=True)
    housing_number = models.CharField(max_length=10, blank=True, null=True)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    floor_number = models.CharField(max_length=10, blank=True, null=True)
    user = models.ForeignKey(
        CustomerUser, on_delete=CASCADE, related_name='user', null=True)
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='order_address', null=True
    )

    def __str__(self) -> str:
        return f'{self.street_name}, {self.street_number}'

    class Meta:
        verbose_name_plural = "Addresses"
