from rest_framework import serializers
from .models import *

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractModel
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True}
        }

class PayedSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayedModel
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True}
        }

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True}
        }