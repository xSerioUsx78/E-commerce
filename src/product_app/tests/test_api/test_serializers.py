from django.db.models import Avg

from utils.tests import APITestCase
from review_app.models import Review
from review_app.serializers import ReviewGlobalSerializer
from review_app.choices import Status
from product_app.models import Product
from product_app.serializers import ProductReviewSerializer


class ProductReviewSerializerTestCase(APITestCase):

    def setUp(self):
        super().setUp()

        self.product = Product.objects.create()
        self.serializer = ProductReviewSerializer

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
        total_score = Review.objects.aggregate(
            total_score=Avg("score")
        )['total_score'] or 0
        serializer = self.serializer({
            "total_score": total_score,
            "reviews": ReviewGlobalSerializer(
                reviews,
                many=True
            ).data
        })
        data = serializer.data
        print(data)
        self.assertIn("total_score", data)
        self.assertIn("reviews", data)
        self.assertEqual(data['total_score'], 4.00)
        self.assertEqual(len(data['reviews']), 3)
