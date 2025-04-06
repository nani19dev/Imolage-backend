from django.db import models
import uuid
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser

class AppUserModel(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    #username = None
    email = models.EmailField(unique=True)
    first_name = models.TextField()
    last_name = models.TextField()
    date_of_birth = models.DateField(null=True)
    phone_number = models.CharField(max_length=20)
    address = models.TextField(null=True)
    #USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['username']

class Landlord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.TextField(null=False)
    given_names = models.TextField(null=False)
    email = models.EmailField(unique=True, null=False)
    phone_number = models.CharField(max_length=20)
    address = models.TextField(null=True)
    #landlord_api_key = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    