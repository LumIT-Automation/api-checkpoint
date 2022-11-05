from rest_framework import serializers
from checkpoint.serializers.CheckPoint.CommonDataStruct import  CheckPointServiceAggressiveAgingSerializer


class CheckPointServiceUdpSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["new-name"] = serializers.CharField(max_length=255, required=False)
        self.fields["accept-replies"] = serializers.BooleanField(required=False)
        self.fields["aggressive-aging"] = CheckPointServiceAggressiveAgingSerializer(required=False)
        self.fields["keep-connections-open-after-policy-installation"] = serializers.BooleanField(required=False)
        self.fields["match-by-protocol-signature"] = serializers.BooleanField(required=False)
        self.fields["match-for-any"] = serializers.BooleanField(required=False)
        self.fields["override-default-settings"] = serializers.BooleanField(required=False)
        self.fields["session-timeout"] = serializers.IntegerField(required=False)
        self.fields["source-port"] = serializers.CharField(max_length=64, required=False)
        self.fields["sync-connections-on-cluster"] = serializers.BooleanField(required=False)
        self.fields["use-default-session-timeout"] = serializers.BooleanField(required=False)

        self.fields["set-if-exists"] = serializers.BooleanField(required=False)
        self.fields["details-level"] = serializers.CharField(max_length=64, required=False)
        self.fields["ignore-warnings"] = serializers.BooleanField(required=False)

    uid = serializers.CharField(max_length=255, required=False)
    name = serializers.CharField(max_length=255, required=True)
    port = serializers.CharField(max_length=64, required=True)
    protocol = serializers.CharField(max_length=64, required=False)

    # groups = serializers.JSONField(required=False)
    comments = serializers.CharField(max_length=255, required=False, allow_blank=True)
    color = serializers.CharField(max_length=64, required=False)
    tags = serializers.JSONField(required=False)
