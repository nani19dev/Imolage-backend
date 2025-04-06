from rest_framework import serializers
from .models import *

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyModel
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'landlord': {'read_only': True}
        }

class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApartmentModel
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True}
        }

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomModel
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True}
        }