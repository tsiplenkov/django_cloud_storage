from rest_framework import serializers


from users.models import UserProfile

# User serializer
class RegRespSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("user_id", "email")


class RegSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("email", "password")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = UserProfile.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user
