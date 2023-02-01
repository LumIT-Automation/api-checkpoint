from rest_framework import serializers
from checkpoint.helpers.Utils import CheckString
from checkpoint.serializers.CheckPoint.CommonDataStruct import CheckPointNatSettingsSerializer


class CheckPointHostWebServerConfigSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["listen-standard-port"] = serializers.BooleanField(required=False)
        self.fields["operating-system"] = serializers.CharField(max_length=64, required=False, allow_blank=True)
        self.fields["protected-by"] = serializers.CharField(max_length=255, required=False, allow_blank=True)

        self.fields["additional-ports"] = serializers.JSONField(required=False)
        self.fields["application-engines"] = serializers.JSONField(required=False)

    def to_internal_value(self, data):
        def checkAddRemoveField(d: dict):
            for k in d:
                if k != "add" and k != "remove":
                    raise ValueError('Invalid data. Expected key: "add" or "remove".')
                if isinstance(d[k], str):
                    d[k] = CheckString.check(d[k], 15)
                elif isinstance(d[k], list):
                    d[k] = [CheckString.check(el, 15) for el in d[k]]
                else:
                    raise serializers.ValidationError('Invalid data in "add" or "remove" field.')

        try:
            # These fields can be a string, a list of string or a dict.
            if "additional-ports" in data:
                if isinstance(data["additional-ports"], str):
                    data["additional-ports"] = CheckString.allowedChars(data["additional-ports"], 15, "0123456789")
                elif isinstance(data["additional-ports"], list):
                    data["additional-ports"] = [ CheckString.allowedChars(el, 15, "0123456789") for el in data["additional-ports"]]
                elif isinstance(data["additional-ports"], dict):
                    data["additional-ports"] = checkAddRemoveField(data["additional-ports"])
                else:
                    msg = 'Incorrect type. Expected a string, list or a dict, but got %s'
                    raise serializers.ValidationError(msg % type(data["additional-ports"]).__name__)

            if "application-engines" in data:
                if isinstance(data["application-engines"], str):
                    data["application-engines"] = CheckString.check(data["application-engines"], 15)
                elif isinstance(data["application-engines"], list):
                    data["application-engines"] = [CheckString.check(el, 15) for el in data["application-engines"]]
                elif isinstance(data["application-engines"], dict):
                    data["application-engines"] = checkAddRemoveField(data["application-engines"])
                else:
                    msg = 'Incorrect type. Expected a string, list or a dict, but got %s'
                    raise serializers.ValidationError(msg % type(data["application-engines"]).__name__)

            return data
        except ValueError as v:
            raise serializers.ValidationError from v
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
