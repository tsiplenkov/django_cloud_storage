from django.conf.urls import url
from django.urls import path, include
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("users.urls")),
    path("", include("files.urls")),
    path("", include("authorize.urls")),
    path("", include("openapi_schema.urls")),
    url(
        r"^$",
        RedirectView.as_view(url="schema/swagger-ui", permanent=False),
        name="index",
    ),
]
