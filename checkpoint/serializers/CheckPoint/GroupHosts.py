from rest_framework import serializers


class CheckPointGroupHostsSerializer(serializers.Serializer):
    hosts = serializers.ListField(child=serializers.CharField(max_length=255, required=False), required=False)
