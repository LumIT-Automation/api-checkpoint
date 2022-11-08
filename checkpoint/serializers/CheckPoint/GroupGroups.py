from rest_framework import serializers


class CheckPointGroupGroupsSerializer(serializers.Serializer):
    class GroupListSerializer(serializers.ListField):
        child = serializers.CharField(max_length=255)

    groups = GroupListSerializer()
