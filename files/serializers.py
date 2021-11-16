from rest_framework import serializers
from files.models import UserFile, FILE_TYPES


class UserFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFile
        fields = "__all__"

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    file_type = serializers.ChoiceField(choices=FILE_TYPES)
    size = serializers.IntegerField(min_value=1)
    # file = serializers.FileField()

    def create(self, validated_data):
        """
        Create and return a new `UserFile` instance, given the validated data.
        """
        return UserFile.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing `UserFile` instance, given the validated data.
    #     """
    #     instance.name = validated_data.get("name", instance.name)
    #     instance.file_type = validated_data.get("file_type", instance.file_type)
    #     instance.save()
    #     return instance
