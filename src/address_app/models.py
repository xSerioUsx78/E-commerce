from django.db import models
from django.contrib.auth import get_user_model

from utils.models import TimestampedModel


User = get_user_model()


class Address(TimestampedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="addresses"
    )
    province = models.CharField(
        "استان",
        max_length=50,
        null=True
    )
    city = models.CharField(
        "شهر",
        max_length=50,
        null=True
    )
    address = models.TextField(
        "آدرس",
        null=True
    )
    plaque = models.CharField(
        "پلاک",
        null=True
    )
    unit = models.CharField(
        "واحد",
        null=True,
        blank=True
    )
    postal_code = models.CharField(
        "کد پستی",
        max_length=50,
        null=True,
        blank=True
    )
    default = models.BooleanField(default=False)

    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس ها"
