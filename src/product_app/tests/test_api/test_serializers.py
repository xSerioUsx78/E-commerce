from django.db.models import Avg

from utils.tests import APITestCase
from review_app.models import Review
from review_app.serializers import ReviewGlobalSerializer
from review_app.choices import Status as ReviewStatus
from question_answer_app.models import QuestionAnswer
from question_answer_app.serializers import QuestionAnswerGlobalSerializer
from question_answer_app.choices import Status as QuestionAnswerStatus
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
            status=ReviewStatus.APPROVED
        )
        Review.objects.create(
            product=self.product,
            score=3,
            status=ReviewStatus.APPROVED
        )
        Review.objects.create(
            product=self.product,
            score=4,
            status=ReviewStatus.APPROVED
        )
        reviews = Review.objects.filter(
            product=self.product,
            status=ReviewStatus.APPROVED
        ).select_related(
            "user"
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
            status=ReviewStatus.APPROVED
        ).select_related(
            "user"
        ).order_by(
            "-updated_at"
        )

        serializer = self.serializer(
            reviews,
            many=True
        )
        data = serializer.data
        self.assertEqual(len(data), 0)


class ProductQuestionAnswerSerializerTestCase(APITestCase):

    def setUp(self):
        super().setUp()

        self.product = Product.objects.create()
        self.serializer = QuestionAnswerGlobalSerializer

    def test_serializer_data_success(self):
        qa1 = QuestionAnswer.objects.create(
            product=self.product,
            status=QuestionAnswerStatus.APPROVED
        )
        QuestionAnswer.objects.create(
            product=self.product,
            status=QuestionAnswerStatus.APPROVED,
            reply=qa1
        )
        qa2 = QuestionAnswer.objects.create(
            product=self.product,
            status=QuestionAnswerStatus.APPROVED
        )
        QuestionAnswer.objects.create(
            product=self.product,
            status=QuestionAnswerStatus.APPROVED,
            reply=qa2
        )
        qa3 = QuestionAnswer.objects.create(
            product=self.product,
            status=QuestionAnswerStatus.APPROVED
        )
        QuestionAnswer.objects.create(
            product=self.product,
            status=QuestionAnswerStatus.APPROVED,
            reply=qa3
        )
        question_answers = QuestionAnswer.objects.filter(
            product=self.product,
            status=QuestionAnswerStatus.APPROVED,
            replies__status=QuestionAnswerStatus.APPROVED
        ).select_related(
            "user"
        ).prefetch_related(
            "replies"
        ).order_by(
            "-updated_at"
        )
        serializer = self.serializer(
            question_answers,
            many=True
        )
        data = serializer.data
        self.assertEqual(len(data), 3)
        for obj in data:
            self.assertIn('user', obj)
            self.assertIn('replies', obj)
            self.assertIn('content', obj)

            for reply in obj['replies']:
                self.assertIn('user', reply)
                self.assertIn('content', reply)
                self.assertNotIn('replies', reply)

    def test_serializer_data_empty_success(self):
        question_answers = QuestionAnswer.objects.filter(
            product=self.product,
            status=ReviewStatus.APPROVED
        ).order_by(
            "-updated_at"
        )

        serializer = self.serializer(
            question_answers,
            many=True
        )
        data = serializer.data
        self.assertEqual(len(data), 0)
