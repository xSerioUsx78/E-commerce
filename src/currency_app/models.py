from django.db import models

from utils.models import TimestampedModel


class CurrencyRate(TimestampedModel):
    currency = models.CharField(
        max_length=3,
        verbose_name="ارز",
        null=True
    )
    rate = models.BigIntegerField(
        verbose_name="نرخ",
        null=True
    )

    class Meta:
        verbose_name = "نرخ ارز"
        verbose_name_plural = "نرخ ارزها"
