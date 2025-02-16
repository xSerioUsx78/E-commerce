from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField

from utils.models import TimestampedModel


User = get_user_model()


def product_image_directory_path(instance, filename):
    return 'product/images/{0}/{1}'.format(instance.id, filename)


class Product(TimestampedModel):
    user = models.ForeignKey(
        User,
        related_name="products",
        on_delete=models.SET_NULL,
        null=True
    )
    title = models.CharField(
        "عنوان",
        max_length=256,
        null=True
    )
    summary = RichTextField(
        "خلاصه توضحیات",
        null=True
    )
    description = RichTextField(
        "توضیحات",
        null=True
    )
    image = models.ImageField(
        "تصویر اصلی",
        null=True,
        upload_to=product_image_directory_path
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True
    )
    discount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        default=0
    )

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self) -> str:
        return self.title or str(self.id)


def product_image_image_directory_path(instance, filename):
    return 'product/images/{0}/addon/{1}'.format(instance.id, filename)


class ProductImage(TimestampedModel):
    user = models.ForeignKey(
        User,
        related_name="product_images",
        on_delete=models.SET_NULL,
        null=True
    )
    product = models.ForeignKey(
        Product,
        related_name="images",
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        "تصویر",
        null=True,
        upload_to=product_image_image_directory_path
    )

    class Meta:
        verbose_name = "عکس محصول"
        verbose_name_plural = "عکس های محصول"

    def __str__(self) -> str:
        return self.product.image if self.product else str(self.id)


class ProductVariation(TimestampedModel):
    user = models.ForeignKey(
        User,
        related_name="product_variations",
        on_delete=models.SET_NULL,
        null=True
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variations"
    )
    title = models.CharField(
        max_length=256,
        null=True
    )

    class Meta:
        verbose_name = "متغیر"
        verbose_name_plural = "متغیرها"

    def __str__(self) -> str:
        return self.title or str(self.id)


class ProductVariationItem(TimestampedModel):
    user = models.ForeignKey(
        User,
        related_name="product_variation_items",
        on_delete=models.SET_NULL,
        null=True
    )
    product_variation = models.ForeignKey(
        ProductVariation,
        on_delete=models.CASCADE,
        related_name="items"
    )
    name = models.CharField(
        max_length=256,
        null=True
    )
    value = models.CharField(
        max_length=256,
        null=True,
        blank=True
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        default=0
    )

    class Meta:
        verbose_name = "آیتم متغیر"
        verbose_name_plural = "آیتم های متغیر"

    def __str__(self) -> str:
        return f'{self.name}: {self.value}' if self.name and self.value else str(self.id)


class ProductSpecification(TimestampedModel):
    user = models.ForeignKey(
        User,
        related_name="product_specifications",
        on_delete=models.SET_NULL,
        null=True
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="specifications"
    )
    title = models.CharField(
        max_length=256,
        null=True
    )

    class Meta:
        verbose_name = "مشخصات"
        verbose_name_plural = "مشخصات"

    def __str__(self) -> str:
        return self.title or str(self.id)


class ProductSpecificationItem(TimestampedModel):
    user = models.ForeignKey(
        User,
        related_name="product_specification_items",
        on_delete=models.SET_NULL,
        null=True
    )
    product_specification = models.ForeignKey(
        ProductSpecification,
        on_delete=models.CASCADE,
        related_name="items"
    )
    name = models.CharField(
        max_length=256,
        null=True
    )
    value = models.CharField(
        max_length=256,
        null=True
    )

    class Meta:
        verbose_name = "آیتم مشخصات"
        verbose_name_plural = "آیتم های مشخصات"

    def __str__(self) -> str:
        return f'{self.name}: {self.value}' if self.name and self.value else str(self.id)
