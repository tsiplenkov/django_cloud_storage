from rest_framework import generics, permissions
from rest_framework.response import Response

from authorize.serializers import RegisterSerializer, RegisterResponseSerializer


class RegisterApiView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [
        permissions.AllowAny,
    ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            RegisterResponseSerializer(user, context=self.get_serializer_context()).data
        )
