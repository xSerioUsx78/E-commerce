from django.db.models import Avg

from utils.tests import APITestCase
from review_app.models import Review
from review_app.serializers import ReviewGlobalSerializer
from review_app.choices import Status
from product_app.models import Product


class ProductReviewSerializerTestCase(APITestCase):

    def setUp(self):
        super().setUp()

        self.product = Product.objects.create()
        self.serializer = ReviewGlobalSerializer

    def test_serializer_data_success(self):
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
        reviews = Review.objects.filter(
            product=self.product,
            status=Status.APPROVED
        ).order_by(
            "-updated_at"
        )
        serializer = self.serializer(
            reviews,
            many=True
        )
        data = serializer.data
        self.assertEqual(len(data), 3)
        for obj in data:
            self.assertIn('user', obj)
            self.assertIn('description', obj)
            self.assertIn('score', obj)

    def test_serializer_data_empty_success(self):
        reviews = Review.objects.filter(
            product=self.product,
            status=Status.APPROVED
        ).order_by(
            "-updated_at"
        )

        serializer = self.serializer(
            reviews,
            many=True
        )
        data = serializer.data
        self.assertEqual(len(data), 0)
