from rest_framework import serializers

from . import models


class QuestionAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.QuestionAnswer
        fields = (
            "product",
            "reply",
            "content"
        )


class QuestionAnswerRepliesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.QuestionAnswer
        fields = (
            "user",
            "content"
        )


class QuestionAnswerGlobalSerializer(serializers.ModelSerializer):

    replies = QuestionAnswerRepliesSerializer(many=True)

    class Meta:
        model = models.QuestionAnswer
        fields = (
            "user",
            "replies",
            "content"
        )
