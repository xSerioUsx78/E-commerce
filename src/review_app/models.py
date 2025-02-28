from django.db import models
from django.contrib.auth import get_user_model
from model_utils.fields import StatusField, MonitorField

from utils.models import TimestampedModel
from product_app.models import Product
from . import choices


User = get_user_model()


class Review(TimestampedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="reviews",
        verbose_name="کاربر"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="محصول"
    )
    description = models.TextField(
        verbose_name="توضیحات",
        null=True,
        blank=True
    )
    score = models.PositiveSmallIntegerField(
        verbose_name="امتیاز",
        null=True
    )
    STATUS = choices.Status.choices
    status = StatusField(
        null=True
    )
    status_changed_at = MonitorField(
        monitor='status',
        when=[
            choices.Status.APPROVED,
            choices.Status.REJECTED,
            choices.Status.PENDING
        ],
        null=True
    )

    class Meta:
        verbose_name = "بازخورد"
        verbose_name_plural = "بازخورد ها"

    def __str__(self):
        return str(self.id)
