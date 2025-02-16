from django.db.models import Sum, F
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from . import serializers
from . import models


class OrderItemViewSet(
    viewsets.GenericViewSet
):
    permission_classes = (permissions.IsAuthenticated, )

    @action(
        ["POST"],
        detail=False,
        url_path="action",
        url_name="action",
        serializer_class=serializers.OrderItemActionSerializer
    )
    def perform_action(self):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        order_item_id = serializer.perform_action()
        return Response({
            "message": "Action performed successfully.",
            "order_item_id": order_item_id
        })


class OrderViewSet(
    viewsets.GenericViewSet
):

    @action(
        methods=['GET'],
        detail=False,
        url_path="cart",
        serializer_class=serializers.OrderCartSerializer,
        permission_classes=(permissions.IsAuthenticated, )
    )
    def cart(self):
        obj = models.Order.objects.filter(
            user=self.request.user
        ).annotate(
            total_price_calculated=Sum(
                F("items__product__price") * F("items__quantity"),
                distinct=True
            ) + Sum(F("items__product_variation_items__price")),
            total_discount_calculated=Sum(
                F("items__product__discount") * F("items__quantity"),
                distinct=True
            )
        ).prefetch_related(
            "items__product",
            "items__product_variation_items",
            "items__product_variation_items__product_variation"
        ).first()

        serializer = self.get_serializer(obj)
        return Response(serializer.data)
