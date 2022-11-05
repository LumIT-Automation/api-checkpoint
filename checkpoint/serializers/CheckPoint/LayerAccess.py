from rest_framework import serializers


class CheckPointLayerAccessSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["new-name"] = serializers.CharField(max_length=255, required=False)
        self.fields["add-default-rule"] = serializers.BooleanField(required=False)
        self.fields["applications-and-url-filtering"] = serializers.BooleanField(required=False)
        self.fields["content-awareness"] = serializers.BooleanField(required=False)
        self.fields["detect-using-x-forward-for"] = serializers.BooleanField(required=False)
        self.fields["implicit-cleanup-action"] = serializers.CharField(max_length=64, required=False)
        self.fields["mobile-access"] = serializers.BooleanField(required=False)

        self.fields["details-level"] = serializers.CharField(max_length=64, required=False)
        self.fields["ignore-warnings"] = serializers.BooleanField(required=False)

    uid = serializers.CharField(max_length=255, required=False)
    name = serializers.CharField(max_length=255, required=True)
    firewall = serializers.BooleanField(required=False)
    shared = serializers.BooleanField(required=False)
    comments = serializers.CharField(max_length=255, required=False, allow_blank=True)
    color = serializers.CharField(max_length=64, required=False)
    tags = serializers.JSONField(required=False)
