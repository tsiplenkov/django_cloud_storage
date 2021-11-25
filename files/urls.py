from django.conf.urls import url

from files.views import UserFileList, UserFileDetail, DownloadViewSet, PublicUserFile

urlpatterns = [
    url(r"^files$", UserFileList.as_view(), name="files-list"),
    url(
        r"^files/(?P<file_id>[a-z0-9-]+)$", UserFileDetail.as_view(), name="file-detail"
    ),
    url(
        r"^files/(?P<file_id>[a-z0-9-]+)/download$",
        DownloadViewSet.as_view({"get": "download"}),
        name="file-download",
    ),
    url(
        r"^public/(?P<public_id>[a-z0-9-]+)$",
        PublicUserFile.as_view({"get": "download"}),
        name="public-file-download",
    ),
]
