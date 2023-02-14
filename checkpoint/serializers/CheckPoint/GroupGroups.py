from rest_framework import serializers


class CheckPointGroupGroupsSerializer(serializers.Serializer):
    groups = serializers.ListField(
        child=serializers.CharField(max_length=255, required=False), required=False
    )
