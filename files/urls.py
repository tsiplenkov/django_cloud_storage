from django.conf.urls import url

from files.views import UserFileList, UserFileDetail

urlpatterns = [
    url(r'^files/$', UserFileList.as_view(), name='files-list'),
    url(r'^files/(?P<file_id>[a-z0-9-]+)/$', UserFileDetail.as_view(), name='file-detail'),
]