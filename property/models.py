from django.db import models
import uuid
from core.models import AppUserModel
#from polymorphic.models import PolymorphicModel

class BuildingModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.TextField(null=True)
    type = models.CharField(max_length=100)
    description = models.TextField(null=True)
    status = models.CharField(max_length=50, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True 

class PropertyModel(BuildingModel):
    landlord = models.ManyToManyField(AppUserModel)

class ApartmentModel(BuildingModel):
    #size_sqft = models.IntegerField()
    property = models.ForeignKey(PropertyModel, on_delete=models.CASCADE)

class RoomModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    type = models.CharField(max_length=100)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    apartment = models.ForeignKey(ApartmentModel, on_delete=models.CASCADE)