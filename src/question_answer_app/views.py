from rest_framework import permissions
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin

from . import serializers
from . import models


class QuestionAnswerViewSet(
    CreateModelMixin,
    UpdateModelMixin,
    GenericViewSet
):
    serializer_class = serializers.QuestionAnswerSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = models.QuestionAnswer.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
