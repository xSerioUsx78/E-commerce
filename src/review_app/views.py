from rest_framework import permissions
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, ListModelMixin

from . import serializers
from . import models


class ReviewViewSet(
    CreateModelMixin,
    UpdateModelMixin,
    GenericViewSet
):
    serializer_class = serializers.ReviewSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = models.Review.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
