from rest_framework import permissions
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin

from . import serializers


class ReviewViewSet(
    GenericViewSet,
    CreateModelMixin,
    UpdateModelMixin
):
    serializer_class = serializers.ReviewSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
