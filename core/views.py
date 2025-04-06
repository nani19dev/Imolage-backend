from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *

#AppUser
class CreateAppUserView(generics.CreateAPIView):
    queryset = AppUserModel.objects.all()
    serializer_class = AppUserSerializer
    permission_classes = [AllowAny] 
