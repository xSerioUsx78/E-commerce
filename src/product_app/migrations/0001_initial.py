# Generated by Django 5.1.6 on 2025-02-10 00:12

import ckeditor.fields
import django.db.models.deletion
import product_app.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=256, null=True, verbose_name='عنوان')),
                ('summary', ckeditor.fields.RichTextField(null=True, verbose_name='خلاصه توضحیات')),
                ('description', ckeditor.fields.RichTextField(null=True, verbose_name='توضیحات')),
                ('image', models.ImageField(null=True, upload_to=product_app.models.product_image_directory_path, verbose_name='تصویر اصلی')),
                ('price', models.PositiveBigIntegerField(null=True)),
                ('discount', models.PositiveBigIntegerField(null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'محصول',
                'verbose_name_plural': 'محصولات',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(null=True, upload_to=product_app.models.product_image_image_directory_path, verbose_name='تصویر')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='product_app.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_images', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'عکس محصول',
                'verbose_name_plural': 'عکس های محصول',
            },
        ),
        migrations.CreateModel(
            name='ProductSpecification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=256, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specifications', to='product_app.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_specifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'مشخصات',
                'verbose_name_plural': 'مشخصات',
            },
        ),
        migrations.CreateModel(
            name='ProductSpecificationItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=256, null=True)),
                ('value', models.CharField(max_length=256, null=True)),
                ('product_specification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='product_app.productspecification')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_specification_items', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'آیتم مشخصات',
                'verbose_name_plural': 'آیتم های مشخصات',
            },
        ),
        migrations.CreateModel(
            name='ProductVariation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=256, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variations', to='product_app.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_variations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'متغیر',
                'verbose_name_plural': 'متغیرها',
            },
        ),
        migrations.CreateModel(
            name='ProductVariationItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=256, null=True)),
                ('value', models.CharField(max_length=256, null=True)),
                ('price', models.PositiveBigIntegerField(default=0, null=True)),
                ('product_variation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='product_app.productvariation')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_variation_items', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'آیتم متغیر',
                'verbose_name_plural': 'آیتم های متغیر',
            },
        ),
    ]
