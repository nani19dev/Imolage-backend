from django.urls import path, include
from . import views

urlpatterns = [
    path("health/", views.health_check, name="health-check"),
    #path("landlords/", views.LandlordListCreate.as_view(), name="create-landlord"),
    #path("landlords/<uuid:pk>/", views.LandlordRetrieveUpdateDestroy.as_view(), name="update-landlord"),
]