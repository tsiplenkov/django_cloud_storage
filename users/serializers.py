# from django.contrib.auth.models import User , Group
from users.models import UserProfile
from rest_framework import serializers


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("__all__")


class UserProfileUsedSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("used_space",)

    # def update(self, instance, validated_data):
    #     instance.email = validated_data.get('used_space', instance.used_space)
    #     instance.save()
    #     print('update')
    #     return instance

#
# class GroupSerializer(field_serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ("url", "name")
