from utils.tests import APITestCase
from currency_app.tasks import currency_rate_modify_task
from currency_app.models import CurrencyRate


class CurrencyRateModifyTaskTestCase(APITestCase):

    def test_currency_rate_modify_success(self):
        currency_rate_modify_task()

        currency_rate = CurrencyRate.objects.first()
        self.assertTrue(currency_rate)
        self.assertTrue(currency_rate.rate)
