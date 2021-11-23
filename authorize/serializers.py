from rest_framework import serializers


# Register serializer
from users.models import UserProfile


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("id", "email", "password")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = UserProfile.objects.create_user(
            validated_data["email"],
            password=validated_data["password"],
        )
        return user


# User serializer
class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("user_id", "email")
