from rest_framework import serializers

from . import models


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Address
        exclude = ("user", )
        read_only_fields = ("default", )
