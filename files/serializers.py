from rest_framework import serializers
from files.models import UserFile


class UserFileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    filename = serializers.ReadOnlyField()
    filesize = serializers.ReadOnlyField()
    public_url = serializers.ReadOnlyField()

    class Meta:
        model = UserFile
        fields = (
            "file_id",
            "owner",
            "file_parent_id",
            "file_object",
            "created_time",
            "public_access",
            "public_url",
            "filename",
            "filesize",
        )

    def to_representation(self, instance):
        representation = super(UserFileSerializer, self).to_representation(instance)
        representation["owner"] = instance.owner.email
        return representation
