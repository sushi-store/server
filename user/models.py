from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.deletion import CASCADE
from phonenumber_field.modelfields import PhoneNumberField
from order.models import Order


class AccountManager(BaseUserManager):

    def create_user(self, email, name, phone_number, password, **other_fields):

        if not email:
            raise ValueError('You must provide an email address.')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name,
                          phone_number=phone_number, **other_fields)
        user.set_password(password)
        user.save()
        pass

    def create_superuser(self, email, name, phone_number, password, **other_fields):

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

        return self.create_user(email, name, phone_number, password, **other_fields)


class CustomerUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    start_date = models.DateTimeField(auto_now=True)

    is_email_confirmed = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['phone_number', 'name']

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        verbose_name_plural = "Users"


class Address(models.Model):
    street_name = models.CharField(max_length=50, blank=True, default='')
    house_number = models.CharField(max_length=10, blank=True, default='')
    entrance_number = models.CharField(max_length=10, blank=True, default='')
    apartments_number = models.CharField(max_length=10, blank=True, default='')
    user = models.ForeignKey(
        CustomerUser, on_delete=CASCADE, related_name='user', null=True)
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='order_address', null=True
    )

    def __str__(self) -> str:
        return f'{self.street_name}, {self.house_number}' if self.street_name and self.house_number else 'No address'

    class Meta:
        verbose_name_plural = "Addresses"
