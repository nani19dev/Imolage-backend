from rest_framework import serializers
from .models import *

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionModel
        fields = '__all__'
        extra_kwargs = {'id': {'read_only': True}}