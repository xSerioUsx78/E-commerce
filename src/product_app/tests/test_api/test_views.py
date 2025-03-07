from rest_framework import status

from utils.tests import APITestCase
from review_app.models import Review
from review_app.choices import Status
from product_app.models import Product


class ProductViewSetTestCase(APITestCase):

    def setUp(self):
        super().setUp()

        self.base_url = "/api/product/"
        self.product = Product.objects.create()
        self.product2 = Product.objects.create()

    def test_reviews_success(self):
        Review.objects.create(
            product=self.product,
            score=5,
            status=Status.APPROVED
        )
        Review.objects.create(
            product=self.product,
            score=3,
            status=Status.APPROVED
        )
        Review.objects.create(
            product=self.product,
            score=4,
            status=Status.APPROVED
        )
        url = f'{self.base_url}{self.product.pk}/reviews/'
        res = self.client.get(url)
        self.assertTrue(res.status_code == status.HTTP_200_OK)
        json = res.json()
        self.assertIn('count', json)
        self.assertIn('next', json)
        self.assertIn('previous', json)
        self.assertIn('results', json)
        self.assertEqual(len(json['results']), 3)
