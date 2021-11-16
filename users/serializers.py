# from django.contrib.auth.models import User , Group
from users.models import UserProfile
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("public_id", "email")

#
# class GroupSerializer(field_serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ("url", "name")
