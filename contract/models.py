from datetime import datetime
from django.db import models
import uuid
from core.models import AppUserModel
from property.models import ApartmentModel, PropertyModel

class ContractModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    rent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    current_rent_payed = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=50, default='active')
    #terms_and_conditions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #property = models.ForeignKey(PropertyModel, on_delete=models.CASCADE, null=True)
    apartment = models.ForeignKey(ApartmentModel, on_delete=models.CASCADE, null=True)
    landlord = models.ManyToManyField(AppUserModel, related_name='tenant_contracts', default=[])
    tenant = models.ManyToManyField(AppUserModel, related_name='landlord_contracts', default=[])

    def calculate_duration(self):
        current_date = datetime.now().date()
        start_date = self.start_date
        # Calculate the difference in years and months
        years_diff = current_date.year - start_date.year
        months_diff = current_date.month - start_date.month
        # Handle cases where the current month is before the start month
        #if months_diff < 0:
            #return 0
            #years_diff -= 1
            #months_diff += 12
        # Combine years and months into total months
        total_months = years_diff * 12 + months_diff
        if total_months < 0:
            return 0
        return total_months #(current_date - start_date)

    def current_rent_due(self):
        return self.calculate_duration() * self.rent
        
    #def current_balance(self):
    #    return self.current_rent_due() - self.current_rent_payed
    
    def current_balance(self):
        return self.current_rent_payed - self.current_rent_due()

class PayedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    contract = models.ForeignKey(ContractModel, on_delete=models.CASCADE)
    current_payed_rent = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class Tenant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.TextField()
    given_names = models.TextField(null=False)
    #national_register = models.TextField(null=False)
    email = models.EmailField(unique=True, null=False)
    phone_number = models.CharField(max_length=20)
    address = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)