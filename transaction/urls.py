from django.urls import path, include
from . import views

urlpatterns = [
    path("contracts/<uuid:contract_id>/transactions/", views.TransactionListCreate.as_view(), name="create-transaction"),
    path("transactions/<uuid:pk>/", views.TransactionRetrieveUpdateDestroy.as_view(), name="update-transaction"),
]