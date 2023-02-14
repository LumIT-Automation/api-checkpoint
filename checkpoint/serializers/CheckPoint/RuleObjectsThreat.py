from rest_framework import serializers


class CheckPointRuleObjectsThreatSerializer(serializers.Serializer):
    source = serializers.JSONField(required=False)
    destination = serializers.JSONField(required=False)
