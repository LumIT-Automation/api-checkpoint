from rest_framework import serializers


class CheckPointVpnToHostSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["ipv4-address"] = serializers.IPAddressField(protocol='IPv4', required=True)
