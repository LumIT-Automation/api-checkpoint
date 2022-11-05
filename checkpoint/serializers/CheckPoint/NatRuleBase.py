from rest_framework import serializers


class CheckPointNatRuleBaseSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["install-on"] = serializers.JSONField(required=False)
        self.fields["rule-number"] =  serializers.CharField(max_length=255, required=False)
        self.fields["original-destination"] = serializers.CharField(max_length=255, required=False)
        self.fields["original-service"] = serializers.CharField(max_length=255, required=False)
        self.fields["original-source"] = serializers.CharField(max_length=255, required=False)
        self.fields["translated-destination"] = serializers.CharField(max_length=255, required=False)
        self.fields["translated-service"] = serializers.CharField(max_length=255, required=False)
        self.fields["translated-source"] = serializers.CharField(max_length=255, required=False)
        self.fields["new-name"] = serializers.CharField(max_length=255, required=False)
        self.fields["new-position"] = serializers.JSONField(required=False)
        self.fields["details-level"] = serializers.CharField(max_length=64, required=False)
        self.fields["ignore-warnings"] = serializers.BooleanField(required=False)

    uid = serializers.CharField(max_length=255, required=False)
    package = serializers.CharField(max_length=255, required=False)
    position = serializers.JSONField(required=False)
    name = serializers.CharField(max_length=255, required=False)
    enabled = serializers.BooleanField(required=False)
    method = serializers.CharField(max_length=64, required=False)
    comments = serializers.CharField(max_length=255, required=False, allow_blank=True)
