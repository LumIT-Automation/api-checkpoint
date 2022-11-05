from rest_framework import serializers


class CheckPointApplicationSiteSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["additional-categories"] = serializers.JSONField(required=False)
        self.fields["new-name"] = serializers.CharField(max_length=255, required=False)
        self.fields["primary-category"] = serializers.CharField(max_length=64, required=False)
        self.fields["url-list"] = serializers.JSONField(required=False)
        self.fields["application-signature"] = serializers.CharField(max_length=4096, required=False)
        self.fields["urls-defined-as-regular-expression"] = serializers.BooleanField(required=False)

    uid = serializers.CharField(max_length=255, required=False)
    name = serializers.CharField(max_length=255, required=True)
    risk = serializers.CharField(max_length=255, required=False)
    description = serializers.CharField(max_length=2048, allow_blank=True, required=False)

    # groups = serializers.JSONField(required=False)
    comments = serializers.CharField(max_length=255, required=False, allow_blank=False)
    color = serializers.CharField(max_length=64, required=False)
    tags = serializers.JSONField(required=False)
