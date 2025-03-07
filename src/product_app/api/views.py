from django.db.models import Avg
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from product_app import serializers
from review_app.models import Review
from review_app.choices import Status
from review_app.serializers import ReviewGlobalSerializer


class ProductViewSet(
    GenericViewSet
):

    @action(
        ["GET"],
        detail=True,
        url_path="reviews",
        url_name="reviews",
        serializer_class=serializers.ProductReviewSerializer
    )
    def reviews(self, request, pk):
        """
        TODO:
            Paginate reviews.
        """
        obj = self.get_object()
        reviews = Review.objects.filter(
            product=obj,
            status=Status.APPROVED
        ).order_by(
            "-updated_at"
        )
        total_score = Review.objects.aggregate(
            total_score=Avg("score")
        )['total_score'] or 0
        serializer = self.get_serializer({
            "total_score": total_score,
            "reviews": ReviewGlobalSerializer(
                reviews,
                many=True
            )
        })
        return Response(serializer.data)
