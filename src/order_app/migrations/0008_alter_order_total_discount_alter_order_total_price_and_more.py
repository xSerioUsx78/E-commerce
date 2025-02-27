# Generated by Django 5.1.6 on 2025-02-13 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_app', '0007_alter_order_total_discount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_discount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='total_discount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='total_price',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True),
        ),
    ]
