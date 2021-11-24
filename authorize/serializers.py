from rest_framework import serializers


from users.models import UserProfile

# User serializer
class RegisterResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("user_id", "email")


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("email", "password")
        # TODO: not working for docs (drf-yasg) request model https://github.com/axnsan12/drf-yasg/issues/70
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = UserProfile.objects.create_user(
            validated_data["email"],
            password=validated_data["password"],
        )
        return user
