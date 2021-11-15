# from django.contrib.auth.models import User
from users.models import UserProfile
from rest_framework import viewsets
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = UserProfile.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer


# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
