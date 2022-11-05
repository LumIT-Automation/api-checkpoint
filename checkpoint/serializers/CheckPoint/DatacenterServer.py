from rest_framework import serializers


class CheckPointDatacenterServersSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["new-name"] = serializers.CharField(max_length=255, required=False)
        self.fields["details-level"] = serializers.CharField(max_length=64, required=False)
        self.fields["ignore-warnings"] = serializers.BooleanField(required=False)

        # AWS datacenter server parameters.
        self.fields["authentication-method"] = serializers.CharField(max_length=64, required=False)
        self.fields["access-key-id"] = serializers.CharField(max_length=255, required=False)
        self.fields["secret-access-key"] = serializers.CharField(max_length=1024, required=False)
        self.fields["region"] = serializers.CharField(max_length=64, required=False)

        # vCenter datacenter server parameters.
        self.fields["username"] = serializers.CharField(max_length=64, required=False)
        self.fields["password-base64"] = serializers.CharField(max_length=255, required=False)
        self.fields["hostname"] = serializers.CharField(max_length=255, required=False)
        self.fields["certificate-fingerprint"] = serializers.CharField(max_length=1024, required=False)

    uid = serializers.CharField(max_length=255, required=False)
    name = serializers.CharField(max_length=255, required=True)
    type = serializers.CharField(max_length=64, required=True)

    # groups = serializers.JSONField(required=False)
    comments = serializers.CharField(max_length=255, required=False, allow_blank=True)
    color = serializers.CharField(max_length=64, required=False)
    tags = serializers.JSONField(required=False)
