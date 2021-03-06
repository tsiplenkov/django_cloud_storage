from rest_framework.response import Response


from users.models import UserProfile
from rest_framework import viewsets, permissions, generics, status
from users.serializers import UserProfileSerializer, SelfUserProfileSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)


class SelfUserProfileDetailView(generics.GenericAPIView):
    http_method_names = ["get", "patch", "delete"]
    serializer_class = SelfUserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user_profile = self.request.user
        serializer = SelfUserProfileSerializer(user_profile)
        return Response(serializer.data)

    def patch(self, request):
        user_profile = self.request.user
        serializer = SelfUserProfileSerializer(
            user_profile, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user_profile = self.request.user
        user_profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
