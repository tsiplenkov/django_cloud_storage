from django.conf.urls import url

from users.views import UserViewSet

user_list = UserViewSet.as_view({"get": "list"})
user_detail = UserViewSet.as_view({"get": "retrieve"})

urlpatterns = [
    url(r"^users/$", user_list, name="userprofile-list"),
    url(r"^users/(?P<pk>[0-9]+)/$", user_detail, name="userprofile-detail"),
]
