from rest_framework import serializers


class CheckPointRuleObjectsHttpsSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["site-category"] = serializers.JSONField(required=False)
        self.fields["site-category-negate"] = serializers.BooleanField(required=False)
        self.fields["destination-negate"] = serializers.BooleanField(required=False)
        self.fields["service-negate"] = serializers.BooleanField(required=False)
        self.fields["source-negate"] = serializers.BooleanField(required=False)
        self.fields["details-level"] = serializers.CharField(max_length=64, required=False)
        self.fields["ignore-warnings"] = serializers.BooleanField(required=False)

    uid = serializers.CharField(max_length=255, required=False)
    name = serializers.CharField(max_length=255, required=False)
    layer = serializers.CharField(max_length=255, required=False)
    destination = serializers.JSONField(required=False)
    service = serializers.JSONField(required=False)
    source = serializers.JSONField(required=False)
