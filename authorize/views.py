from rest_framework import generics, permissions
from rest_framework.response import Response

from authorize.serializers import RegisterSerializer, RegisterResponseSerializer


class RegisterApiView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny,]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data
        # return Response(
        #     {
        #         "user": RegisterResponseSerializer(
        #             user, context=self.get_serializer_context()
        #         ).data,
        #         "message": "User Created Successfully.  Now perform Login to get your token",
        #     }
        # )
