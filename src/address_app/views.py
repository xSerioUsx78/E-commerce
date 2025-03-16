from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from . import serializers
from . import models


class AddressViewSet(viewsets.ModelViewSet):
    queryset = models.Address.objects.all().order_by('-created_at')
    serializer_class = serializers.AddressSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return super().get_queryset().filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        methods=['PUT', 'PATCH'],
        detail=True,
        url_path="make-default",
        serializer_class=None
    )
    def make_default(self, request, pk):
        models.Address.objects.filter(
            default=True
        ).update(
            default=False
        )
        models.Address.objects.filter(
            pk=pk
        ).update(
            default=True
        )
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
