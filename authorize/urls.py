from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from authorize.views import RegApiView

urlpatterns = [
    path("auth/login", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/registration", RegApiView.as_view(), name="user_registration"),
]
