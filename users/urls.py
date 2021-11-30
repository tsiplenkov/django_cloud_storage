from django.conf.urls import url

from users.views import UserViewSet, SelfUserProfileDetailView

urlpatterns = [
    url(r"^users$", UserViewSet.as_view({"get": "list"}), name="userprofile-list"),
    url(
        r"^users/(?P<pk>[0-9]+)$",
        UserViewSet.as_view({"get": "retrieve"}),
        name="userprofile-detail",
    ),
    url(r"^users/self$", SelfUserProfileDetailView.as_view(), name="userself-detail")
]
