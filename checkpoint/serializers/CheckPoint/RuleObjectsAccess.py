from rest_framework import serializers


class CheckPointRuleObjectsAccessSerializer(serializers.Serializer):
    source = serializers.JSONField(required=False)
    destination = serializers.JSONField(required=False)
