# Generated by Django 5.1.6 on 2025-02-11 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_app', '0004_alter_order_total_discount_alter_order_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.PositiveIntegerField(default=1, null=True),
        ),
    ]
