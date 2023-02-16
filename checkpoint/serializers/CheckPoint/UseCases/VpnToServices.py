from rest_framework import serializers


class CheckPointVpnToServicesSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"] = serializers.CharField(max_length=255, required=False)
