# Generated by Django 5.1.6 on 2025-02-13 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0002_alter_product_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariationitem',
            name='value',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
