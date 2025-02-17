from django.db import models
from model_utils.fields import StatusField, MonitorField

from utils.models import TimestampedModel
from order_app.models import Order
from . import choices
from . import helpers


class Payment(TimestampedModel):
    order = models.OneToOneField(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        related_name="payments"
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True
    )
    ref_id = models.CharField(
        default=helpers.generate_random_payment_ref_id,
        max_length=6,
        null=True
    )
    addon_data = models.JSONField(
        default=dict,
        blank=True,
        null=True
    )
    STATUS = choices.Status.choices
    status = StatusField(
        null=True
    )
    finished_at = MonitorField(
        monitor='status',
        when=[
            choices.Status.SUCCESS,
            choices.Status.FAILED
        ],
        null=True
    )

    class Meta:
        verbose_name = "پرداخت"
        verbose_name_plural = "پرداخت ها"
