from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

from product_app.models import Product
from review_app.models import Review
from review_app.choices import Status as ReviewStatus
from review_app.serializers import ReviewGlobalSerializer
from question_answer_app.models import QuestionAnswer
from question_answer_app.choices import Status as QuestionAnswerStatus
from question_answer_app.serializers import QuestionAnswerGlobalSerializer


class ProductViewSet(
    GenericViewSet
):
    queryset = Product.objects.all()

    @action(
        ["GET"],
        detail=True,
        url_path="reviews",
        url_name="reviews",
        serializer_class=ReviewGlobalSerializer
    )
    def reviews(self, request, pk):
        obj = self.get_object()
        reviews = Review.objects.filter(
            product=obj,
            status=ReviewStatus.APPROVED
        ).order_by(
            "-updated_at"
        )
        page = self.paginate_queryset(reviews)
        serializer = self.get_serializer(
            page,
            many=True
        )
        reviews_response = self.get_paginated_response(serializer.data)
        return reviews_response

    @action(
        ["GET"],
        detail=True,
        url_path="questions-answers",
        url_name="questions-answers",
        serializer_class=QuestionAnswerGlobalSerializer
    )
    def quesions_answers(self, request, pk):
        obj = self.get_object()
        quesions_answers = QuestionAnswer.objects.filter(
            product=obj,
            status=QuestionAnswerStatus.APPROVED
        ).order_by(
            "-updated_at"
        )
        page = self.paginate_queryset(quesions_answers)
        serializer = self.get_serializer(
            page,
            many=True
        )
        quesions_answers_response = self.get_paginated_response(
            serializer.data
        )
        return quesions_answers_response
