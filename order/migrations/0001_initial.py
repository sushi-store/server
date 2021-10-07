# Generated by Django 3.2.5 on 2021-10-07 12:58

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sushi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('delivery_type', models.CharField(choices=[('P', 'Pickup'), ('D', 'Delivery')], default='D', max_length=1)),
                ('payment_method', models.CharField(choices=[('C', 'Cash'), ('D', 'Card')], default='С', max_length=1)),
                ('user_id', models.PositiveIntegerField(default=None, null=True)),
                ('uuid', models.CharField(default=None, max_length=50, null=True)),
                ('status', models.CharField(choices=[('P', 'Pending'), ('I', 'In Process'), ('D', 'Done'), ('C', 'Cancelled')], default='P', max_length=1)),
                ('date_of_order', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='order.order')),
                ('sushi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sushi', to='sushi.sushi')),
            ],
            options={
                'verbose_name_plural': 'Sushi Orders',
                'unique_together': {('order', 'sushi')},
            },
        ),
    ]
