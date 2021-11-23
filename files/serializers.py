from rest_framework import serializers
from files.models import UserFile


class UserFileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    filename = serializers.ReadOnlyField()
    filesize = serializers.ReadOnlyField()

    class Meta:
        model = UserFile
        fields = (
            "file_id",
            "owner",
            "file_parent_id",
            "file_object",
            "created_time",
            "access_link",
            "filename",
            "filesize",
        )

    def to_representation(self, instance):
        representation = super(UserFileSerializer, self).to_representation(instance)
        representation["owner"] = instance.owner.email
        return representation
