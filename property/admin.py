from django.contrib import admin
from .models import *

admin.site.register(PropertyModel)
admin.site.register(ApartmentModel)
admin.site.register(RoomModel)