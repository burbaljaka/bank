from rest_framework import serializers

class OperationSerializer(serializers.Serializer):
    user = serializers.UUIDField()
    action = serializers.CharField()
