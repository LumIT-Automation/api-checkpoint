from rest_framework import serializers


class CheckPointRuleBaseHttpsSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["rule-number"] =  serializers.CharField(max_length=255, required=False)
        self.fields["destination-negate"] = serializers.BooleanField(required=False)
        self.fields["install-on"] = serializers.JSONField(required=False)
        # self.fields["new-name"] = serializers.CharField(max_length=255, required=True)
        self.fields["new-position"] = serializers.JSONField(required=False)
        self.fields["service-negate"] = serializers.BooleanField(required=False)
        self.fields["site-category"] = serializers.JSONField(required=False)
        self.fields["site-category-negate"] = serializers.BooleanField(required=False)
        self.fields["source-negate"] = serializers.BooleanField(required=False)

        self.fields["details-level"] = serializers.CharField(max_length=64, required=False)
        self.fields["ignore-warnings"] = serializers.BooleanField(required=False)

    uid = serializers.CharField(max_length=255, required=False)
    name = serializers.CharField(max_length=255, required=False)
    position = serializers.JSONField(required=False)
    layer = serializers.CharField(max_length=255, required=False)
    destination = serializers.JSONField(required=False)
    service = serializers.JSONField(required=False)
    source = serializers.JSONField(required=False)
    action = serializers.CharField(max_length=64, required=False)
    blade = serializers.JSONField(required=False)
    certificate = serializers.CharField(max_length=255, required=False)
    enabled = serializers.BooleanField(required=False)
    track = serializers.CharField(max_length=64, required=False)
    comments = serializers.CharField(max_length=255, required=False, allow_blank=True)
