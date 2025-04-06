from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import *
from .serializers import *
from contract.models import PayedModel

#Transaction
class TransactionListCreate(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated] #[AllowAny]

    def get_queryset(self):
        contract_id = self.kwargs.get('contract_id')
        return TransactionModel.objects.filter(contract__id=contract_id).order_by('-date')

    def create(self, request, contract_id):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            #transaction_type = request.data.get('type')
            #allowed_types = ['rent', 'maintenance']
            #if transaction_type not in allowed_types:
                #raise serializers.ValidationError({"type": [f"Transaction type must be one of: {', '.join(allowed_types)}."]})
            transaction = serializer.save()
            contract = transaction.contract
            if transaction.type == 'rent':
                contract.current_rent_payed += transaction.amount #update_current_payed_rent(payed, transaction)
                contract.save()
            #elif transaction.type == 'maintenance':
                #contract.save()
                #pass
        except Exception as e:
            raise serializers.ValidationError(str(e))
        return Response(status=201)
    
class TransactionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = TransactionModel.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        #DELETE
        try:
            contract = instance.contract
            if instance.type == 'rent':
                contract.current_rent_payed -= instance.amount #update_current_payed_rent(payed, transaction)
                contract.save()
                instance.delete()
        except Exception as e: 
            raise serializers.ValidationError(str(e))
        #CREATE
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            transaction = serializer.save()
            contract = transaction.contract
            if transaction.type == 'rent':
                contract.current_rent_payed += transaction.amount #update_current_payed_rent(payed, transaction)
                contract.save()
        except PayedModel.DoesNotExist:
            raise ValidationError({'id': 'Invalid payed ID'})
        #UPDATE
        #instance = self.get_object()
        #serializer = self.get_serializer(instance, data=request.data, partial=True)
        #serializer.is_valid(raise_exception=True)
        #try:
        #    transaction = serializer.save()
        #    contract = transaction.contract
        #    payed = Payed.objects.get(contract=contract)
        #    payed.current_payed_rent += transaction.amount - instance.amount
        #    payed.save()
        #except Exception as e: 
        #    raise serializers.ValidationError(str(e))
        return Response(serializer.data)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            contract = instance.contract
            if instance.type == 'rent':
                contract.current_rent_payed -= instance.amount
                contract.save()
                instance.delete()
        except Exception as e: 
            raise serializers.ValidationError(str(e))
        return Response(status=204)

#def update_current_payed_rent(payed, transaction):
#    payed.current_payed_rent += transaction.amount

#Transaction
#class TransactionListCreate(generics.ListCreateAPIView):
#    serializer_class = TransactionSerializer
#    permission_classes = [IsAuthenticated] #[AllowAny]
#
#    def get_queryset(self):
#        contract_id = self.kwargs.get('contract_id')
#        return TransactionModel.objects.filter(contract__id=contract_id)
#
#    def create(self, request):
#        serializer = self.get_serializer(data=request.data)
#        serializer.is_valid(raise_exception=True)
#        try:
#            transaction = serializer.save()
#            contract = transaction.contract
#            payed = PayedModel.objects.get(contract=contract)
#            payed.current_payed_rent += transaction.amount #update_current_payed_rent(payed, transaction)
#            payed.save()
#        except PayedModel.DoesNotExist:
#            raise ValidationError({'id': 'Invalid payed ID'})
#        return Response(serializer.data)

#class TransactionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#    queryset = TransactionModel.objects.all()
#    serializer_class = TransactionSerializer
#    permission_classes = [IsAuthenticated]
#    lookup_field = "pk"
#
#    def update(self, request, *args, **kwargs):
#        instance = self.get_object()
#        #DELETE
#        try:
#            contract = instance.contract
#            payed = PayedModel.objects.get(contract=contract)
#            payed.current_payed_rent -= instance.amount #update_current_payed_rent(payed, transaction)
#            payed.save()
#            instance.delete()
#        except Exception as e: 
#            raise serializers.ValidationError(str(e))
#        #CREATE
#        serializer = self.get_serializer(data=request.data)
#        serializer.is_valid(raise_exception=True)
#        try:
#            transaction = serializer.save()
#            contract = transaction.contract
#            payed = PayedModel.objects.get(contract=contract)
#            payed.current_payed_rent += transaction.amount #update_current_payed_rent(payed, transaction)
#            payed.save()
#        except PayedModel.DoesNotExist:
#            raise ValidationError({'id': 'Invalid payed ID'})
#        #UPDATE
#        #instance = self.get_object()
#        #serializer = self.get_serializer(instance, data=request.data, partial=True)
#        #serializer.is_valid(raise_exception=True)
#        #try:
#        #    transaction = serializer.save()
#        #    contract = transaction.contract
#        #    payed = Payed.objects.get(contract=contract)
#        #    payed.current_payed_rent += transaction.amount - instance.amount
#        #    payed.save()
#        #except Exception as e: 
#        #    raise serializers.ValidationError(str(e))
#        return Response(serializer.data)
#    
#    def delete(self, request, *args, **kwargs):
#        instance = self.get_object()
#        try:
#            contract = instance.contract
#            payed = PayedModel.objects.get(contract=contract)
#            payed.current_payed_rent -= instance.amount
#            payed.save()
#            instance.delete()
#        except Exception as e: 
#            raise serializers.ValidationError(str(e))
#        return Response(status=204)
