from rest_framework import serializers


class  CheckPointActionSettingsSerializer(serializers.Serializer):
    uid = serializers.BooleanField(required=False)
    limit = serializers.CharField(max_length=255, required=False)



class CheckPointCustomFieldsSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["field-1"] = serializers.CharField(max_length=255, required=False)
        self.fields["field-2"] = serializers.CharField(max_length=255, required=False)
        self.fields["field-3"] = serializers.CharField(max_length=255, required=False)



class CheckPointTrackSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["enable-firewall-session"] = serializers.BooleanField(required=False)
        self.fields["per-connection"] = serializers.BooleanField(required=False)
        self.fields["per-session"] = serializers.BooleanField(required=False)

    accounting = serializers.BooleanField(required=False)
    alert = serializers.CharField(max_length=64, required=False)
    type = serializers.CharField(max_length=64, required=False)



class  CheckPointCustomFrequencySerializer(serializers.Serializer):
    every = serializers.IntegerField(required=False)
    unit = serializers.CharField(max_length=64, required=False)



class CheckPointUserCheckSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["custom-frequency"] = CheckPointCustomFrequencySerializer(required=False)

    confirm = serializers.CharField(max_length=64, required=False)
    frequency = serializers.CharField(max_length=64, required=False)
    interaction = serializers.CharField(max_length=255, required=False)



class CheckPointRuleBaseAccessSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["rule-number"] = serializers.IntegerField(required=False)
        self.fields["action-settings"] = CheckPointActionSettingsSerializer(required=False)
        self.fields["content-direction"] = serializers.CharField(max_length=64, required=False)
        self.fields["content-negate"] = serializers.BooleanField(required=False)
        self.fields["custom-fields"] = CheckPointCustomFieldsSerializer(required=False)
        self.fields["destination-negate"] = serializers.BooleanField(required=False)
        self.fields["inline-layer"] = serializers.CharField(max_length=255, required=False)
        self.fields["install-on"] = serializers.JSONField(required=False)
        self.fields["new-name"] = serializers.CharField(max_length=255, required=False)
        self.fields["new-position"] = serializers.JSONField(required=False)
        self.fields["service-negate"] = serializers.BooleanField(required=False)
        self.fields["service-resource"] = serializers.CharField(max_length=255, required=False)
        self.fields["source-negate"] = serializers.BooleanField(required=False)
        self.fields["user-check"] = CheckPointUserCheckSerializer(required=False)
        self.fields["details-level"] = serializers.CharField(max_length=64, required=False)
        self.fields["ignore-warnings"] = serializers.BooleanField(required=False)

    uid = serializers.CharField(max_length=255, required=False)
    name = serializers.CharField(max_length=255, required=False)
    layer = serializers.CharField(max_length=255, required=False)
    position = serializers.JSONField(required=False)
    action = serializers.CharField(max_length=64, required=False)
    content = serializers.JSONField(required=False)
    destination = serializers.JSONField(required=False)
    enabled = serializers.BooleanField(required=False)
    service = serializers.JSONField(required=False)
    source = serializers.JSONField(required=False)
    time = serializers.JSONField(required=False)
    track = CheckPointTrackSerializer(required=False)
    vpn = serializers.JSONField(required=False)
    comments = serializers.CharField(max_length=255, required=False, allow_blank=True)
