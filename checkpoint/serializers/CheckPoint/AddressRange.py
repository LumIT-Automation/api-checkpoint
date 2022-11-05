from rest_framework import serializers
from checkpoint.serializers.CheckPoint.CommonDataStruct import CheckPointNatSettingsSerializer


class CheckPointAddressRangeSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["ipv4-address-first"] = serializers.IPAddressField(required=False)
        self.fields["ipv4-address-last"] = serializers.IPAddressField(required=False)
        self.fields["ipv6-address-first"] = serializers.IPAddressField(required=False)
        self.fields["ipv6-address-last"] = serializers.IPAddressField(required=False)
        self.fields["nat-settings"] = CheckPointNatSettingsSerializer(required=False)
        self.fields["new-name"] = serializers.CharField(max_length=255, required=False)

        self.fields["set-if-exists"] = serializers.BooleanField(required=False)
        self.fields["ignore-warnings"] = serializers.BooleanField(required=False)
        self.fields["set-if-exists"] = serializers.BooleanField(required=False)

    uid = serializers.CharField(max_length=255, required=False)
    name = serializers.CharField(max_length=255, required=True)
    comments = serializers.CharField(max_length=255, required=False, allow_blank=False)
    color = serializers.CharField(max_length=64, required=False)
    tags = serializers.JSONField(required=False)
