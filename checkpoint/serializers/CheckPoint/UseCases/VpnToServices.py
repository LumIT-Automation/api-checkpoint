from rest_framework import serializers


class CheckPointVpnToServicesSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=True)
