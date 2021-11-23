# from django.contrib.auth.models import User
from users.models import UserProfile
from rest_framework import viewsets
from users.serializers import UserProfileSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Этот набор представлений автоматически создает действия `list` и `detail`.
    """

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
