# Generated by Django 3.2.5 on 2021-08-09 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sushi', '0001_initial'),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='order.order'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='sushi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sushi', to='sushi.sushi'),
        ),
    ]
