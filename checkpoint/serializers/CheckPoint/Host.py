from rest_framework import serializers

from checkpoint.serializers.CheckPoint.CommonDataStruct import CheckPointNatSettingsSerializer

from checkpoint.helpers.Exception import CustomException
from checkpoint.helpers.Log import Log


class CheckPointHostAddRemoveFieldSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for k in kwargs["data"]:
            if k in ("add", "remove"):
                if isinstance(kwargs["data"][k], list):
                    self.fields[k] = serializers.ListField(child=serializers.CharField(max_length=64, required=False), required=False)
                elif isinstance(kwargs["data"][k], str):
                    self.fields[k] = serializers.CharField(max_length=64, required=False, allow_blank=True)
                else:
                    raise CustomException(status=400, payload={"CheckPoint": "Invalid data for key \"" + k + "\". Expected a list or a string."})
            else:
                raise CustomException(status=400, payload={"CheckPoint": "Invalid data. Expected dictionary key: \"add\" or \"remove\", got \"" + k + "\"."})



class CheckPointHostWebServerConfigSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["listen-standard-port"] = serializers.BooleanField(required=False)
        self.fields["operating-system"] = serializers.CharField(max_length=64, required=False, allow_blank=True)
        self.fields["protected-by"] = serializers.CharField(max_length=255, required=False, allow_blank=True)

        # These fields can be either a string, a list of string or a dict.
        if "additional-ports" in kwargs["data"]:
            if isinstance(kwargs["data"]["additional-ports"], str):
                self.fields["additional-ports"] =  serializers.CharField(max_length=255, required=False)
            elif isinstance(kwargs["data"]["additional-ports"], list):
                self.fields["additional-ports"] = serializers.ListField(child=serializers.CharField(max_length=255, required=False), required=False)
            elif isinstance(kwargs["data"]["additional-ports"], dict):
                AdditionalPortsAddRemoveFieldArgs = dict()
                AdditionalPortsAddRemoveFieldArgs["data"] = kwargs.get("data", {}).get("additional-ports", {})
                AdditionalPortsAddRemoveFieldArgs["required"] = False

                self.fields["additional-ports"] = CheckPointHostAddRemoveFieldSerializer(**AdditionalPortsAddRemoveFieldArgs)
            else:
                msg = 'Incorrect type. Expected a string, list or a dict, but got %s'
                raise serializers.ValidationError(msg % type(kwargs["data"]["additional-ports"]).__name__)

        if "application-engines" in kwargs["data"]:
            if isinstance(kwargs["data"]["application-engines"], str):
                self.fields["application-engines"] = serializers.CharField(max_length=255, required=False)
            elif isinstance(kwargs["data"]["application-engines"], list):
                self.fields["application-engines"] = serializers.ListField(child=serializers.CharField(max_length=255, required=False), required=False)
            elif isinstance(kwargs["data"]["application-engines"], dict):
                ApplicationEnginesAddRemoveFieldArgs = dict()
                ApplicationEnginesAddRemoveFieldArgs["data"] = kwargs.get("data", {}).get("application-engines", {})
                ApplicationEnginesAddRemoveFieldArgs["required"] = False

                self.fields["application-engines"] = CheckPointHostAddRemoveFieldSerializer(**ApplicationEnginesAddRemoveFieldArgs)
            else:
                msg = 'Incorrect type. Expected a string, list or a dict, but got %s'
                raise serializers.ValidationError(msg % type(kwargs["data"]["application-engines"]).__name__)



class CheckPointHostServerSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        WebServerConfigArg = dict()
        WebServerConfigArg["data"] = kwargs.get("data", {}).get("web-server-config", {})
        WebServerConfigArg["required"] = False

        self.fields["dns-server"] = serializers.BooleanField(required=False)
        self.fields["mail-server"] = serializers.BooleanField(required=False)
        self.fields["web-server"] = serializers.BooleanField(required=False)
        self.fields["web-server-config"] =  CheckPointHostWebServerConfigSerializer(**WebServerConfigArg)



class CheckPointHostSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        HostServerConfigArgs = dict()
        HostServerConfigArgs["data"] = kwargs.get("data", {}).get("host-servers", {})
        HostServerConfigArgs["required"] = False

        self.fields["ipv4-address"] = serializers.IPAddressField(required=True)
        self.fields["ipv6-address"] = serializers.IPAddressField(required=False)
        self.fields["nat-settings"] = CheckPointNatSettingsSerializer(required=False)
        self.fields["new-name"] = serializers.CharField(max_length=255, required=False)
        self.fields["host-servers"] = CheckPointHostServerSerializer(**HostServerConfigArgs)

        self.fields["set-if-exists"] = serializers.BooleanField(required=False)
        self.fields["details-level"] = serializers.CharField(max_length=64, required=False)
        self.fields["ignore-warnings"] = serializers.BooleanField(required=False)

    uid = serializers.CharField(max_length=255, required=False)
    name = serializers.CharField(max_length=255, required=True)
    interfaces = serializers.JSONField(required=False)
    comments = serializers.CharField(max_length=255, required=False, allow_blank=True)
    color = serializers.CharField(max_length=64, required=False)
    tags = serializers.JSONField(required=False)
