from rest_framework import serializers

from checkpoint.serializers.Permission.IdentityGroup import IdentityGroupSerializer


class IdentityGroupsSerializer(serializers.Serializer):
    items = IdentityGroupSerializer(many=True)
