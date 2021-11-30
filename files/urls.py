from django.conf.urls import url

from files.views import UserFileListView, UserFileDetailView, DownloadViewSet, PublicUserFileViewSet

urlpatterns = [
    url(r"^files$", UserFileListView.as_view(), name="files-list"),
    url(
        r"^files/(?P<file_id>[a-z0-9-]+)$", UserFileDetailView.as_view(), name="file-detail"
    ),
    url(
        r"^files/(?P<file_id>[a-z0-9-]+)/download$",
        DownloadViewSet.as_view({"get": "download"}),
        name="file-download",
    ),
    url(
        r"^public/(?P<public_id>[a-z0-9-]+)$",
        PublicUserFileViewSet.as_view({"get": "download"}),
        name="public-file-download",
    ),
]
