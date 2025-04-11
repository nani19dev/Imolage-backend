from django.urls import path, include
from . import views

urlpatterns = [
    path("properties/", views.PropertyListCreate.as_view(), name="create-property"),
    path("properties/<uuid:pk>/", views.PropertyRetrieveUpdateDestroy.as_view(), name="update-property"),
    path("properties/<uuid:property_id>/apartments/", views.ApartmentListCreate.as_view(), name="create-apartment"),
    path("apartments/<uuid:pk>/", views.ApartmentRetrieveUpdateDestroy.as_view(), name="update-apartment"),
    #path("rooms/", views.RoomListCreate.as_view(), name="create-room"),
    #path("rooms/<uuid:pk>/", views.RoomRetrieveUpdateDestroy.as_view(), name="update-room"),
]