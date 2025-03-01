from rest_framework import status

from utils.tests import APITestCase
from product_app.models import Product
from review_app.models import Review


class ReviewViewSetTestCase(APITestCase):

    def setUp(self):
        super().setUp()

        self.base_url = "/api/review/"

        self.product = Product.objects.create()

    def test_create_review_success(self):
        self.authenticate(self.user)

        data = {
            "product": self.product.pk,
            "score": 5,
            "description": "Test Description"
        }

        res = self.client.post(
            self.base_url,
            data
        )
        self.assertEqual(
            res.status_code,
            status.HTTP_201_CREATED
        )

        review = Review.objects.first()
        self.assertTrue(review)
        self.assertEqual(self.user, review.user)
        self.assertEqual(data['product'], review.product.pk)
        self.assertEqual(data['score'], review.score)
        self.assertEqual(data['description'], review.description)

    def test_update_review_different_user_fail(self):
        self.authenticate(self.user2)

        review = Review.objects.create(
            user=self.user,
            product=self.product,
            score=1
        )

        data = {
            "product": self.product.pk,
            "score": 5,
            "description": "Test Description"
        }

        url = f'{self.base_url}{review.pk}/'

        res = self.client.put(
            url,
            data
        )
        self.assertEqual(
            res.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_update_review_success(self):
        self.authenticate(self.user)

        review = Review.objects.create(
            user=self.user,
            product=self.product,
            score=1
        )

        data = {
            "product": self.product.pk,
            "score": 5,
            "description": "Test Description"
        }

        url = f'{self.base_url}{review.pk}/'

        res = self.client.put(
            url,
            data
        )
        self.assertEqual(
            res.status_code,
            status.HTTP_200_OK
        )

        review.refresh_from_db()
        self.assertTrue(review)
        self.assertEqual(data['product'], review.product.pk)
        self.assertEqual(data['score'], review.score)
        self.assertEqual(data['description'], review.description)
