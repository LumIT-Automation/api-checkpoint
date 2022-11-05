from rest_framework import serializers
from checkpoint.serializers.CheckPoint.CommonDataStruct import CheckPointNatSettingsSerializer


class CheckPointNetworkSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["mask-length4"] = serializers.IntegerField(required=False)
        self.fields["mask-length6"] = serializers.IntegerField(required=False)
        self.fields["subnet-mask"] = serializers.CharField(max_length=64, required=False)
        self.fields["nat-settings"] = CheckPointNatSettingsSerializer(required=False)
        self.fields["new-name"] = serializers.CharField(max_length=255, required=False)

        self.fields["set-if-exists"] = serializers.BooleanField(required=False)
        self.fields["details-level"] = serializers.CharField(max_length=64, required=False)
        self.fields["ignore-warnings"] = serializers.BooleanField(required=False)

    uid = serializers.CharField(max_length=255, required=False)
    name = serializers.CharField(max_length=255, required=True)
    broadcast = serializers.CharField(max_length=64, required=False)
    subnet4 = serializers.IPAddressField(required=False)
    subnet6 = serializers.IPAddressField(required=False)
    # groups = serializers.JSONField(required=False)
    comments = serializers.CharField(max_length=255, required=False, allow_blank=True)
    color = serializers.CharField(max_length=64, required=False)
    tags = serializers.JSONField(required=False)
