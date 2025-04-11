from django.contrib import admin
from django.urls import path, include
from core.views import CreateAppUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/register/", CreateAppUserView.as_view(), name= "register"),
    path("api/token/", TokenObtainPairView.as_view(), name= "get_token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name= "refresh"),
    path("api-auth/", include("rest_framework.urls")),
    path("api/core/", include("core.urls")),
    path("api/property/", include('property.urls')),
    path("api/contract/", include('contract.urls')),
    path("api/transaction/", include('transaction.urls')),
]
