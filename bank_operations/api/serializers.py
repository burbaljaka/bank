from rest_framework import serializers
from .models import *

class OperationSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    amount = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

# class TransactionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Transaction
#         fields = '__all__'