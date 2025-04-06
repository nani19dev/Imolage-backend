from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import *
from .serializers import *

#Contract
class ContractListCreate(generics.ListCreateAPIView):
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated] #[AllowAny]

    def get_queryset(self):
        apartment_id = self.kwargs.get('apartment_id')
        return ContractModel.objects.filter(apartment__id=apartment_id)

class ContractRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = ContractModel.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

class ContractBalanceRetrieve(generics.RetrieveAPIView):
    queryset = ContractModel.objects.all()
    serializer_class = ContractSerializer  # Or a dedicated BalanceSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    #def get_queryset(self):
    #    contract_id = self.kwargs.get('pk')
    #    return ContractModel.objects.get(pk=contract_id)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()  
        return Response({
            'balance': instance.current_balance()
        })

#Payed
class PayedRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = PayedModel.objects.all()
    serializer_class = PayedSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "contract_id"

#Tenant
class TenantListCreate(generics.ListCreateAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [IsAuthenticated]

class TenantRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"