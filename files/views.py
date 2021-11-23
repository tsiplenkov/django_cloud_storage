from django.http import Http404
from rest_framework import status, generics, permissions
from rest_framework.response import Response

from files.models import UserFile
from files.serializers import UserFileSerializer
from users.serializers import UserProfileUsedSpaceSerializer


class UserFileList(generics.ListCreateAPIView):
    def get_queryset(self):
        # after get all products on DB it will be filtered by its owner and return the queryset
        owner_queryset = self.queryset.filter(owner=self.request.user)
        return owner_queryset

    queryset = UserFile.objects.get_queryset()
    serializer_class = UserFileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ["get", "post"]

    def get(self, request):
        queryset = self.get_queryset()
        serializer = UserFileSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        user_file_serializer = UserFileSerializer(data=request.data)
        UserProfile = self.request.user
        for filename in request.FILES:
            file_size = request.FILES[filename].size
            max_disk_space = UserProfile.disk_space
            current_used_space = UserProfile.used_space
            if (max_disk_space - current_used_space) < file_size:
                return Response('storage limit exceeded', status=status.HTTP_400_BAD_REQUEST)
            new_used_space = current_used_space + file_size
            used_space_serializer = UserProfileUsedSpaceSerializer(
                UserProfile, data={"used_space": str(new_used_space)}, partial=True
            )
            if used_space_serializer.is_valid():
                used_space_serializer.save()

        if user_file_serializer.is_valid():
            user_file_serializer.save(
                owner=self.request.user,
            )
            return Response(user_file_serializer.data, status=status.HTTP_201_CREATED)
        return Response(user_file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserFileDetail(generics.RetrieveDestroyAPIView):
    http_method_names = ["get", "delete"]
    serializer_class = UserFileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, file_id):
        try:
            return UserFile.objects.get(file_id=file_id)
        except UserFile.DoesNotExist:
            raise Http404

    def get(self, request, file_id):
        UserFile = self.get_object(file_id)
        serializer = UserFileSerializer(UserFile)
        return Response(serializer.data)

    # def put(self, request, file_id):
    #     UserFile = self.get_object(file_id)
    #     serializer = UserFileSerializer(UserFile, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, file_id):
        UserFile = self.get_object(file_id)
        UserProfile = self.request.user
        file_size = UserFile.filesize
        current_used_space = UserProfile.used_space
        new_used_space = current_used_space - file_size
        used_space_serializer = UserProfileUsedSpaceSerializer(
            UserProfile, data={"used_space": str(new_used_space)}, partial=True
        )
        UserFile.delete()
        if used_space_serializer.is_valid():
            used_space_serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
