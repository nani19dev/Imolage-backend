from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from .models import *
from .serializers import *

#AppUser
class CreateAppUserView(generics.CreateAPIView):
    queryset = AppUserModel.objects.all()
    serializer_class = AppUserSerializer
    permission_classes = [AllowAny] 

def health_check(request):
    """Simple health check endpoint for Docker/Dokploy liveness checks."""
    return JsonResponse({"status": "ok"})
