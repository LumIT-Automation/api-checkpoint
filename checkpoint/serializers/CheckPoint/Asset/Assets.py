from rest_framework import serializers

from checkpoint.serializers.CheckPoint.Asset.Asset import CheckPointAssetSerializer


class CheckPointAssetsSerializer(serializers.Serializer):
    class CheckPointAssestItems(serializers.Serializer):
        id = serializers.IntegerField(required=True)
        address = serializers.CharField(max_length=64, required=True) # @todo: only valid data.
        fqdn = serializers.CharField(max_length=255, required=True) # @todo: only valid data.
        baseurl = serializers.CharField(max_length=255, required=True)
        tlsverify = serializers.IntegerField(required=True)
        datacenter = serializers.CharField(max_length=255, required=True)
        environment = serializers.CharField(max_length=255, required=True)
        position = serializers.CharField(max_length=255, required=True)

    items = CheckPointAssetSerializer(many=True)
