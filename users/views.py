# from django.contrib.authorize.models import User
from users.models import UserProfile
from rest_framework import viewsets, permissions
from users.serializers import UserProfileSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)


# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
