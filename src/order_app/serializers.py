from django.db.models import F
from rest_framework import serializers

from product_app.models import Product, ProductVariationItem
from product_app.serializers import ProductGlobalSerializer, ProductVariationItemGlobalSerializer
from order_app.models import Order
from address_app.models import Address
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


class OrderPaySerializer(serializers.Serializer):

    address = serializers.IntegerField(
        min_value=1,
        required=False,
        allow_null=True
    )
    method = serializers.ChoiceField(
        choices=[
            ("zarinpal", "Zarinpal"),
            ("card_to_card", "Card to card"),
            ("crypto", "Crypto")
        ],
        required=True
    )

    class Meta:
        fields = (
            'address',
        )

    def validate(self, attrs):
        """
        TODO:
            Maybe we need to validate some fields that related to each other.
        """
        attrs = super().validate(attrs)

        address = attrs.get('address')

        request = self.context['request']

        if address:
            address = Address.objects.filter(
                user=request.user,
                id=address
            ).first()
            if not address:
                serializers.ValidationError("آدرس یافت نشد.")
            attrs['address'] = address

        return attrs

    def create_payment(self):
        """
        TODO:
            We should check the method payment and create link or doing whatever needed
            to procced the payment.
        NOTE:
            For now we only return a test link address.
        """
        request = self.context['request']
        order = Order.objects.filter(
            user=request.user
        ).first()
        if not order:
            raise serializers.ValidationError("سفارش یافت نشد.")

        data = self.validated_data
        address = data.get('address')

        if address:
            order.address = address

        """
        TODO:
            Create payment and return a link.
        """

        return {"payment_link": "http://localhost:8000"}
