from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from files import views

urlpatterns = [
    url(r"^files/$", views.UserFileList.as_view()),
    url(r"^files/(?P<pk>[0-9]+)/$", views.UserFileDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
