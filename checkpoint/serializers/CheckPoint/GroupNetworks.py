from rest_framework import serializers


class CheckPointGroupNetworksSerializer(serializers.Serializer):
    class NetworkListSerializer(serializers.ListField):
        child = serializers.CharField(max_length=255)

    networks = NetworkListSerializer()
