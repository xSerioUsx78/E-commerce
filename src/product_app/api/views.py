from django.db.models import Avg
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from product_app.models import Product
from product_app import serializers
from review_app.models import Review
from review_app.choices import Status
from review_app.serializers import ReviewGlobalSerializer


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
            status=Status.APPROVED
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
