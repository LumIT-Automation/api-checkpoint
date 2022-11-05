from rest_framework import serializers


class CheckPointTrackSettingsSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["packet-capture"] = serializers.BooleanField(required=False)



class CheckPointRuleBaseThreatSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["rule-number"] = serializers.IntegerField(required=False)
        self.fields["destination-negate"] = serializers.BooleanField(required=False)
        self.fields["install-on"] = serializers.JSONField(required=False)
        self.fields["new-name"] = serializers.CharField(max_length=255, required=False)
        self.fields["new-position"] = serializers.JSONField(required=False)
        self.fields["protected-scope"] = serializers.JSONField(required=False)
        self.fields["protected-scope-negate"] = serializers.BooleanField(required=False)
        self.fields["service-negate"] = serializers.BooleanField(required=False)
        self.fields["source-negate"] = serializers.BooleanField(required=False)
        self.fields["track-settings"] = serializers.JSONField(required=False)
        self.fields["details-level"] = serializers.CharField(max_length=64, required=False)
        self.fields["ignore-warnings"] = serializers.BooleanField(required=False)

    uid = serializers.CharField(max_length=255, required=False)
    name = serializers.CharField(max_length=255, required=False)
    position = serializers.JSONField(required=False)
    layer = serializers.CharField(max_length=255, required=False)
    action = serializers.CharField(max_length=64, required=False)
    destination = serializers.JSONField(required=False)
    enabled = serializers.BooleanField(required=False)
    service = serializers.JSONField(required=False)
    source = serializers.JSONField(required=False)
    track = serializers.CharField(max_length=64, required=False)
    comments = serializers.CharField(max_length=255, required=False, allow_blank=True)
