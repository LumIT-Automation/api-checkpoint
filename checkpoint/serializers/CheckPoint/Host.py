from rest_framework import serializers
from checkpoint.serializers.CheckPoint.CommonDataStruct import CheckPointNatSettingsSerializer


class CheckPointAddRemoveSerializer(serializers.Serializer):
    add = serializers.JSONField(required=False)
    remove = serializers.JSONField(required=False)

    def to_internal_value(self, data):
        try:
            # These fields can be a string or a list of string.
            if "add" in data:
                if isinstance(data["add"], str):
                    self.fields["add"] = serializers.CharField(max_length=255, required=False)
                elif isinstance(data["add"], list):
                    self.fields["add"] = serializers.ListField(child=serializers.CharField(max_length=255, required=False), required=False)
                else:
                    raise ValueError('Invalid data. Expected a string or a list, but got '+str(type(data["add"])))
            if "remove" in data:
                if isinstance(data["remove"], str):
                    self.fields["remove"] = serializers.CharField(max_length=255, required=False)
                elif isinstance(data["remove"], list):
                    self.fields["remove"] = serializers.ListField(child=serializers.CharField(max_length=255, required=False), required=False)
                else:
                    raise ValueError('Invalid data. Expected a string or a list, but got '+str(type(data["remove"])))

            return super().to_internal_value(data)
        except Exception as e:
            raise e



class CheckPointHostWebServerConfigSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["listen-standard-port"] = serializers.BooleanField(required=False)
        self.fields["operating-system"] = serializers.CharField(max_length=64, required=False, allow_blank=True)
        self.fields["protected-by"] = serializers.CharField(max_length=255, required=False, allow_blank=True)

        self.fields["additional-ports"] = serializers.JSONField(required=False)
        self.fields["application-engines"] = serializers.JSONField(required=False)

    def to_internal_value(self, data):
        try:
            # These fields can be a string, a list of string or a dict.
            if "additional-ports" in data:
                if isinstance(data["additional-ports"], str):
                    self.fields["additional-ports"] = serializers.CharField(max_length=255, required=False)
                elif isinstance(data["additional-ports"], list):
                    self.fields["additional-ports"] = serializers.ListField(child=serializers.CharField(max_length=255, required=False), required=False)
                elif isinstance(data["additional-ports"], dict):
                    self.fields["additional-ports"] = CheckPointAddRemoveSerializer(required=False)
                else:
                    raise ValueError('Invalid data. Expected a string or a list, but got '+str(type(data["additional-ports"])))

            if "application-engines" in data:
                if isinstance(data["application-engines"], str):
                    self.fields["application-engines"] = serializers.CharField(max_length=255, required=False)
                elif isinstance(data["application-engines"], list):
                    self.fields["application-engines"] = serializers.ListField(child=serializers.CharField(max_length=255, required=False), required=False)
                elif isinstance(data["application-engines"], dict):
                    self.fields["application-engines"] = CheckPointAddRemoveSerializer(required=False)
                else:
                    raise ValueError('Invalid data. Expected a string or a list, but got '+str(type(data["application-engines"])))

            return super().to_internal_value(data)
        except Exception as e:
            raise e



class CheckPointHostServerSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["dns-server"] = serializers.BooleanField(required=False)
        self.fields["mail-server"] = serializers.BooleanField(required=False)
        self.fields["web-server"] = serializers.BooleanField(required=False)
        self.fields["web-server-config"] =  CheckPointHostWebServerConfigSerializer(required=False)


class CheckPointHostSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["ipv4-address"] = serializers.IPAddressField(required=True)
        self.fields["ipv6-address"] = serializers.IPAddressField(required=False)
        self.fields["nat-settings"] = CheckPointNatSettingsSerializer(required=False)
        self.fields["new-name"] = serializers.CharField(max_length=255, required=False)
        self.fields["host-servers"] = CheckPointHostServerSerializer(required=False)

        self.fields["set-if-exists"] = serializers.BooleanField(required=False)
        self.fields["details-level"] = serializers.CharField(max_length=64, required=False)
        self.fields["ignore-warnings"] = serializers.BooleanField(required=False)

    uid = serializers.CharField(max_length=255, required=False)
    name = serializers.CharField(max_length=255, required=True)
    interfaces = serializers.JSONField(required=False)
    # groups = serializers.JSONField(required=False)
    comments = serializers.CharField(max_length=255, required=False, allow_blank=True)
    color = serializers.CharField(max_length=64, required=False)
    tags = serializers.JSONField(required=False)
