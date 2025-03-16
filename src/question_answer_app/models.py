from django.db import models
from django.contrib.auth import get_user_model
from model_utils.fields import StatusField, MonitorField

from utils.models import TimestampedModel
from product_app.models import Product
from . import choices


User = get_user_model()


class QuestionAnswer(TimestampedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="questions_answers",
        null=True
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="questions_answers",
        verbose_name="محصول"
    )
    reply = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="replies",
        null=True,
        blank=True
    )
    content = models.TextField(
        verbose_name="پرسش/پاسخ"
    )
    STATUS = choices.Status.choices
    status = StatusField()
    status_changed_at = MonitorField(
        monitor='status',
        when=[
            choices.Status.APPROVED,
            choices.Status.REJECTED,
            choices.Status.PENDING
        ],
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "پرسش و پاسخ"
        verbose_name_plural = "پرسش ها و پاسخ ها"

    def __str__(self):
        return str(self.pk)
