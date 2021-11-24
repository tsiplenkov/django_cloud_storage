from users.models import UserProfile
from rest_framework import serializers


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("user_id", "email", "disk_space", "used_space")


class UserProfileUsedSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("used_space",)


class SelfUserProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(read_only=True)
    disk_space = serializers.IntegerField(read_only=True)
    used_space = serializers.IntegerField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ("user_id", "email", "disk_space", "used_space", "password")
        read_only_fields = ("user_id", "disk_space", "used_space")
        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()

        return instance



#
# class GroupSerializer(field_serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ("url", "name")
