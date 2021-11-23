from django.conf.urls import url
from django.urls import path, include
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns

from cloud_storage.views import api_root

urlpatterns = format_suffix_patterns(
    [
        path("admin/", admin.site.urls),
        url(r"^$", api_root),
        path("api-auth/", include("rest_framework.urls")),
        path("", include("users.urls")),
        path("", include("files.urls")),
    ]
)
