from celery import shared_task

from .brsapi.api import BrsAPI
from . import models


@shared_task
def currency_rate_modify_task():
    """
    Update the currency rate task.
    """

    api = BrsAPI()

    json = api.get_currency_rate(name="دلار")
    if not json:
        return

    price = json.get('price')
    if not price:
        return

    models.CurrencyRate.objects.update_or_create(
        currency="دلار",
        defaults={
            "rate": price
        }
    )
