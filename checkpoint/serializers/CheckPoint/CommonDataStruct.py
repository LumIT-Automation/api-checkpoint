from rest_framework import serializers


class CheckPointNatSettingsSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["auto-rule"] = serializers.BooleanField(required=True)
        self.fields["ipv4-address"] = serializers.IPAddressField(required=False)
        self.fields["ipv6-address"] = serializers.IPAddressField(required=False)
        self.fields["hide-behind"] = serializers.CharField(max_length=64, required=False)
        self.fields["install-on"] = serializers.CharField(max_length=64, required=False)
        self.fields["method"] = serializers.CharField(max_length=64, required=False)



class CheckPointServiceAggressiveAgingSerializer(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["use-default-timeout"] = serializers.BooleanField(required=False)
        self.fields["default-timeout"] = serializers.IntegerField(required=False)

    enable = serializers.BooleanField(required=False)
    timeout = serializers.IntegerField(required=False)
