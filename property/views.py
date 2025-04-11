from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import *
from .serializers import *

#Property
class PropertyListCreate(generics.ListCreateAPIView):
    queryset = PropertyModel.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated] #[AllowAny]
    
    #def get_queryset(self):
    #    user = self.request.user
    #    return Property.objects.filter(landlord=user)
    
    #def perform_create(self, serializer):
    #    if serializer.is_valid():
    #        serializer.save(landlord=self.request.user)
    #    else:
    #        print(serializer.errors)

class PropertyRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = PropertyModel.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    #def get_queryset(self):
    #    user = self.request.user
    #    return Property.objects.filter(landlord=user)

#Apartment
class ApartmentListCreate(generics.ListCreateAPIView):
    serializer_class = ApartmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        property_id = self.kwargs.get('property_id')
        return ApartmentModel.objects.filter(property__id=property_id)

class ApartmentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = ApartmentModel.objects.all()
    serializer_class = ApartmentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

#Room
class RoomListCreate(generics.ListCreateAPIView):
    queryset = RoomModel.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

class RoomRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = RoomModel.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated] 
    lookup_field = "pk"
