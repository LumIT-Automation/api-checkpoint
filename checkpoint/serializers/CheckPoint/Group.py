from rest_framework import serializers


class CheckPointGroupSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["new-name"] = serializers.CharField(max_length=255, required=False)
        self.fields["details-level"] = serializers.CharField(max_length=64, required=False)
        self.fields["ignore-warnings"] = serializers.BooleanField(required=False)

    uid = serializers.CharField(max_length=255, required=False)
    name = serializers.CharField(max_length=255, required=False)
    members = serializers.JSONField(required=False)

    # groups = serializers.JSONField(required=False)
    comments = serializers.CharField(max_length=255, required=False, allow_blank=True)
    color = serializers.CharField(max_length=64, required=False)
    tags = serializers.JSONField(required=False)
