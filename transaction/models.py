from django.db import models
import uuid
from core.models import AppUserModel
from property.models import PropertyModel
from contract.models import ContractModel

class TransactionModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    sender_id = models.ForeignKey(AppUserModel, on_delete=models.CASCADE, null=True)
    #receiver_id = models.ForeignKey(PropertyModel, on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True)
    status = models.CharField(max_length=20, default='pending')
    payment_method = models.CharField(max_length=100)
    #reference_number = models.CharField(max_length=100, null=True)
    date = models.DateTimeField()
    contract = models.ForeignKey(ContractModel, on_delete=models.CASCADE)