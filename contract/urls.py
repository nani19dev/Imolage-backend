from django.urls import path, include
from . import views

urlpatterns = [
    path("apartments/<uuid:apartment_id>/contracts/", views.ContractListCreate.as_view(), name="create-contract"),
    path("contracts/<uuid:pk>/", views.ContractRetrieveUpdateDestroy.as_view(), name="update-contract"),
    path("contracts/<uuid:pk>/balance/", views.ContractBalanceRetrieve.as_view(), name="retrieve-contract-balance"),
]