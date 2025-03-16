from utils.tests import APITestCase
from question_answer_app.models import QuestionAnswer
from question_answer_app.serializers import QuestionAnswerSerializer
from product_app.models import Product


class QuestionAnswerSerializerTestCase(APITestCase):

    def setUp(self):
        super().setUp()

        self.product = Product.objects.create()
        self.serializer = QuestionAnswerSerializer

    def test_field_validation_bad_product_id_fail(self):
        data = {
            "product": 0,
            "content": "Test content"
        }
        serializer = self.serializer(data=data)
        self.assertFalse(serializer.is_valid())
        errors = serializer.errors
        self.assertIn("product", errors)

    def test_field_validation_not_exists_product_id_fail(self):
        data = {
            "product": 999,
            "content": "Test content"
        }
        serializer = self.serializer(data=data)
        self.assertFalse(serializer.is_valid())
        errors = serializer.errors
        self.assertIn("product", errors)

    def test_field_validation_content_is_null_fail(self):
        data = {
            "product": self.product.pk,
            "content": None
        }
        serializer = self.serializer(data=data)
        self.assertFalse(serializer.is_valid())
        errors = serializer.errors
        self.assertIn("content", errors)

    def test_field_validation_content_is_empty_string_fail(self):
        data = {
            "product": self.product.pk,
            "content": ""
        }
        serializer = self.serializer(data=data)
        self.assertFalse(serializer.is_valid())
        errors = serializer.errors
        self.assertIn("content", errors)

    def test_field_validation_bad_reply_id_fail(self):
        data = {
            "product": self.product.pk,
            "reply": 0,
            "content": "Test content"
        }
        serializer = self.serializer(data=data)
        self.assertFalse(serializer.is_valid())
        errors = serializer.errors
        self.assertIn("reply", errors)

    def test_field_validation_not_exists_reply_id_fail(self):
        data = {
            "product": self.product.pk,
            "reply": 999,
            "content": "Test content"
        }
        serializer = self.serializer(data=data)
        self.assertFalse(serializer.is_valid())
        errors = serializer.errors
        self.assertIn("reply", errors)

    def test_create_success_with_reply(self):
        question_answer = QuestionAnswer.objects.create(
            user=self.user,
            product=self.product,
            content="Text content"
        )
        data = {
            "product": self.product.pk,
            "reply": question_answer.pk,
            "content": "Test content"
        }
        serializer = self.serializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_create_success_no_reply(self):
        data = {
            "product": self.product.pk,
            "reply": None,
            "content": "Test content"
        }
        serializer = self.serializer(data=data)
        self.assertTrue(serializer.is_valid())
