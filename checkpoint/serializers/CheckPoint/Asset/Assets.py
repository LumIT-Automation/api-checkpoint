from rest_framework import serializers

from checkpoint.serializers.CheckPoint.Asset.Asset import CheckPointAssetSerializer


class CheckPointAssetsSerializer(serializers.Serializer):
    items = CheckPointAssetSerializer(many=True)
