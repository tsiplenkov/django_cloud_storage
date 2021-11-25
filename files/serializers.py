from rest_framework import serializers
from files.models import UserFile


class UserFileSerializer(serializers.ModelSerializer):
    # TODO: drf-spectacular warning https://github.com/tfranzel/drf-spectacular/issues/68#issuecomment-633741787
    # https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/#updating-our-serializer
    owner = serializers.ReadOnlyField(source="owner.username")


    class Meta:
        model = UserFile
        fields = (
            "file_id",
            "owner",
            "created_time",
            "file_object",
            "public_access",
            "public_url",
            "file_url",
            "filename",
            "filesize",

        )

        read_only_fields = ("owner", "filename", "filesize", "file_url", "public_url")
        extra_kwargs = {"file_object": {"write_only": True}}

    def to_representation(self, instance):
        representation = super(UserFileSerializer, self).to_representation(instance)
        representation["owner"] = instance.owner.email
        return representation

class DownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFile
        fields = ("file_object",)
        read_only_fields = ("file_object",)


class PublicAccessSetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFile
        fields = ("public_access",)
        extra_kwargs = {"public_access": {"write_only": True}}
