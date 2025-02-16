from django.db import models
from django.contrib.auth import get_user_model

from utils.models import TimestampedModel
from product_app.models import Product, ProductVariationItem


User = get_user_model()


class Order(TimestampedModel):
    user = models.ForeignKey(
        User,
        related_name="orders",
        on_delete=models.SET_NULL,
        null=True
    )
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True
    )
    total_discount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        default=0
    )

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش ها"

    def __str__(self) -> str:
        return str(self.id)


class OrderItem(TimestampedModel):
    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        related_name="order_items",
        on_delete=models.SET_NULL,
        null=True
    )
    product_variation_items = models.ManyToManyField(
        ProductVariationItem,
        related_name="order_items",
        null=True
    )
    quantity = models.PositiveIntegerField(
        default=1,
        null=True
    )
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True
    )
    total_discount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        default=0
    )

    class Meta:
        verbose_name = "آیتم سفارش"
        verbose_name_plural = "آیتم های سفارش"

    def __str__(self) -> str:
        return str(self.id)
