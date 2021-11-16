from files.models import UserFile
from files.serializers import UserFileSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UserFileList(APIView):
    """
    Перечисляет все файлы или создает новый файл.
    """

    def get(self, request, format=None):
        files = UserFile.objects.all()
        serializer = UserFileSerializer(files, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserFileDetail(APIView):
    """
    Извлекает, обновляет или удаляет экземпляр сниппета.
    """

    def get_object(self, pk):
        try:
            return UserFile.objects.get(pk=pk)
        except UserFile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        file = self.get_object(pk)
        serializer = UserFileSerializer(file)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        file = self.get_object(pk)
        serializer = UserFileSerializer(file, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        file = self.get_object(pk)
        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
