from rest_framework import generics, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from authorize.serializers import RegSerializer, RegRespSerializer


class RegApiView(generics.GenericAPIView):
    serializer_class = RegSerializer
    permission_classes = [
        permissions.AllowAny,
    ]

    @extend_schema(
        summary="Create a new user",
        responses={
            201: OpenApiResponse(response=RegRespSerializer,
                                 description='Created. New user in response'),
            400: OpenApiResponse(description='Bad request (something invalid)'),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            RegRespSerializer(user, context=self.get_serializer_context()).data,
            status=status.HTTP_201_CREATED,
        )
