from rest_framework import serializers


class AddreddRangesListSerializer(serializers.ListField):
    child = serializers.CharField(max_length=255)



class CheckPointGroupAddressRangesSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["address-ranges"] = AddreddRangesListSerializer()
