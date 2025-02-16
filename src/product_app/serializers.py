from rest_framework import serializers
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
