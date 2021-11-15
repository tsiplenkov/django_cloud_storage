from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from django.conf.urls import url
from users import views

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
# router.register(r"groups", views.GroupViewSet)

# Привязываем наше API используя автоматическую маршрутизацию.
# Также мы подключим возможность авторизоваться в браузерной версии API.

urlpatterns = [
    path("admin/", admin.site.urls),
    url(r"^", include(router.urls)),
    url(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]

