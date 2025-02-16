from django.db.models import F
from rest_framework import serializers

from product_app.models import Product, ProductVariationItem
from product_app.serializers import ProductGlobalSerializer, ProductVariationItemGlobalSerializer
from . import models


class OrderItemActionSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=1)
    product_variation_items_id = serializers.ListField(
        required=False,
        allow_null=True
    )
    action = serializers.ChoiceField(
        choices=[("add", "Add"), ('remove', 'Remove')]
    )

    class Meta:
        fields = (
            'product_id',
            'product_variation_items_id',
            'action'
        )

    def validate(self, attrs):
        attrs = super().validate(attrs)

        product_id = attrs.get('product_id')
        product_variation_items_id = attrs.get(
            'product_variation_items_id', None
        )

        if not Product.objects.filter(id=product_id).exists():
            raise serializers.ValidationError("محصول یافت نشد.")
        if product_variation_items_id and not ProductVariationItem.objects.filter(
            product_variation__product_id=product_id,
            id__in=product_variation_items_id
        ).exists():
            raise serializers.ValidationError("متغیر یا متغیرها یافت نشدند.")

        return attrs

    def perform_action(self):
        product_id = self.validated_data.get('product_id')
        product_variation_items_id = self.validated_data.get(
            'product_variation_items_id',
            None
        )
        action = self.validated_data.get('action')
        user = self.context['request'].user

        order, _ = models.Order.objects.get_or_create(
            user=user
        )

        query_by = {
            "order": order,
            "product_id": product_id
        }
        if product_variation_items_id:
            query_by["product_variation_items__id__in"] = product_variation_items_id
        else:
            query_by["product_variation_items"] = None

        order_item = models.OrderItem.objects.filter(
            **query_by
        ).first()

        if action == "add":
            if not order_item:
                order_item = models.OrderItem.objects.create(
                    order=order,
                    product_id=product_id
                )
                if product_variation_items_id:
                    order_item.product_variation_items.set(
                        product_variation_items_id
                    )
            else:
                order_item.quantity = F("quantity") + 1
                order_item.save(update_fields=['quantity'])

            return order_item.id

        if not order_item:
            return None

        if order_item.quantity <= 1:
            order_item.delete()
        else:
            order_item.quantity = F("quantity") - 1
            order_item.save(update_fields=['quantity'])

        return order_item.id


class OrderItemListSerializer(serializers.ModelSerializer):

    product = ProductGlobalSerializer(read_only=True)
    product_variation_items = ProductVariationItemGlobalSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = models.OrderItem
        fields = (
            'product',
            'product_variation_items',
            'quantity'
        )


class OrderCartSerializer(serializers.ModelSerializer):

    total_price_calculated = serializers.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    total_discount_calculated = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    items = OrderItemListSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = models.Order
        fields = (
            'total_price_calculated',
            'total_discount_calculated',
            'items'
        )
