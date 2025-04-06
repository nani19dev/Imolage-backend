from rest_framework import serializers
from .models import *

class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUserModel
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    
    # hash the password
    def create(self, validated_data):
        user = AppUserModel.objects.create_user(**validated_data)
        return user
    