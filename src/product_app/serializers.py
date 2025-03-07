from rest_framework import serializers

from review_app.serializers import ReviewGlobalSerializer
from . import models


class ProductGlobalSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Product
        fields = ('title', 'price', 'discount')


class ProductVariationGlobalSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProductVariation
        fields = ('title', )


class ProductVariationItemGlobalSerializer(serializers.ModelSerializer):

    product_variation = ProductVariationGlobalSerializer(read_only=True)

    class Meta:
        model = models.ProductVariationItem
        fields = ('product_variation', 'name', 'value')


class ProductReviewSerializer(serializers.Serializer):
    total_score = serializers.DecimalField(
        max_digits=3,
        decimal_places=2,
        read_only=True
    )
    reviews = ReviewGlobalSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        fields = (
            "total_score",
            "reviews"
        )
