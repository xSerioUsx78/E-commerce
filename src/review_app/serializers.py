from rest_framework import serializers

from . import models


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Review
        fields = (
            "product",
            "description",
            "score"
        )


class ReviewGlobalSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Review
        fields = (
            "user",
            "description",
            "score"
        )
