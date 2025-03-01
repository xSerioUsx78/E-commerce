from utils.tests import APITestCase
from review_app.models import Review
from review_app.serializers import ReviewSerializer
from product_app.models import Product


class ReviewSerializerTestCase(APITestCase):

    def setUp(self):
        super().setUp()

        self.product = Product.objects.create()
        self.serializer = ReviewSerializer

    def test_field_validation_bad_product_id_fail(self):
        data = {
            "product": 0,
            "score": 5,
            "description": "Test description"
        }
        serializer = self.serializer(data=data)
        self.assertFalse(serializer.is_valid())
        errors = serializer.errors
        self.assertIn("product", errors)

    def test_field_validation_not_exists_product_id_fail(self):
        data = {
            "product": 999,
            "score": 5,
            "description": "Test description"
        }
        serializer = self.serializer(data=data)
        self.assertFalse(serializer.is_valid())
        errors = serializer.errors
        self.assertIn("product", errors)

    def test_field_validation_score_is_null_fail(self):
        data = {
            "product": self.product.pk,
            "score": None,
            "description": "Test description"
        }
        serializer = self.serializer(data=data)
        self.assertFalse(serializer.is_valid())
        errors = serializer.errors
        self.assertIn("score", errors)

    def test_field_validation_score_is_empty_string_fail(self):
        data = {
            "product": self.product.pk,
            "score": None,
            "description": "Test description"
        }
        serializer = self.serializer(data=data)
        self.assertFalse(serializer.is_valid())
        errors = serializer.errors
        self.assertIn("score", errors)

    def test_field_validation_score_less_than_min_fail(self):
        data = {
            "product": self.product.pk,
            "score": 0,
            "description": "Test description"
        }
        serializer = self.serializer(data=data)
        self.assertFalse(serializer.is_valid())
        errors = serializer.errors
        self.assertIn("score", errors)

    def test_field_validation_score_more_than_max_fail(self):
        data = {
            "product": self.product.pk,
            "score": 6,
            "description": "Test description"
        }
        serializer = self.serializer(data=data)
        self.assertFalse(serializer.is_valid())
        errors = serializer.errors
        self.assertIn("score", errors)

    def test_create_success_with_description(self):
        data = {
            "product": self.product.pk,
            "score": 5,
            "description": "Test description"
        }
        serializer = self.serializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_create_success_no_description(self):
        data = {
            "product": self.product.pk,
            "score": 5,
            "description": None
        }
        serializer = self.serializer(data=data)
        self.assertTrue(serializer.is_valid())
