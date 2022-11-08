from rest_framework import serializers


class CheckPointPolicyPackageLayersSerializer(serializers.Serializer):
    class CheckPointPolicyPackageLayerObjectsSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255, required=True)
        position = serializers.IntegerField(required=True)

    add = CheckPointPolicyPackageLayerObjectsSerializer(required=False, many=True)
    remove = serializers.ListField(child=serializers.CharField(max_length=255, required=False), required=True)
    value = serializers.ListField(child=serializers.IntegerField(required=False), required=True)



class CheckPointPolicyPackageSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["access-layers"] = CheckPointPolicyPackageLayersSerializer(required=False)
        self.fields["desktop-security"] = serializers.BooleanField(required=False)
        self.fields["https-layers"] = serializers.CharField(max_length=255, required=False)
        self.fields["installation-targets"] = serializers.JSONField(required=False)
        self.fields["new-name"] = serializers.CharField(max_length=255, required=False)
        self.fields["qos-policy-type"] = serializers.CharField(max_length=64, required=False)
        self.fields["threat-layers"] = CheckPointPolicyPackageLayersSerializer(required=False)
        self.fields["threat-prevention"] = serializers.BooleanField(required=False)
        self.fields["vpn-traditional-mode"] = serializers.BooleanField(required=False)

        self.fields["details-level"] = serializers.CharField(max_length=64, required=False)
        self.fields["ignore-warnings"] = serializers.BooleanField(required=False)

    uid = serializers.CharField(max_length=255, required=False)
    name = serializers.CharField(max_length=255, required=False)
    access = serializers.BooleanField(required=False)
    qos = serializers.BooleanField(required=False)
    tags = serializers.JSONField(required=False)
    color = serializers.CharField(max_length=64, required=False)
    comments = serializers.CharField(max_length=255, required=False, allow_blank=True)
