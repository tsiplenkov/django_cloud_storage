from django.urls import reverse

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from .serializers import RegSerializer, RegRespSerializer
from users.models import UserProfile


class RegSerializerTestCase(APITestCase):
    def setUp(self):
        self.userprofile_attributes = {"email": "test@test.com", "password": "test123"}

        self.userprofile = UserProfile.objects.create(**self.userprofile_attributes)
        self.serializer = RegSerializer(instance=self.userprofile)

    def test_contains_expected_fields(self):
        data = set(self.serializer.data)

        self.assertEqual(data, {"email"})


class RegRespSerializerTestCase(APITestCase):
    def setUp(self):
        self.userprofile_attributes = {"email": "test@test.com", "password": "test123"}

        self.userprofile = UserProfile.objects.create(**self.userprofile_attributes)
        self.serializer = RegRespSerializer(instance=self.userprofile)

    def test_contains_expected_fields(self):
        data = set(self.serializer.data)

        self.assertEqual(data, {"user_id", "email"})


class RegApiViewTestCase(APITestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.userprofile_data = {"email": "test@test.ru", "password": "1234"}
        self.response = self.client.post(
            reverse("user_registration"),  # urls.urlpatterns name
            self.userprofile_data,
            format="json",
        )

        self.userprofile_bad_data = {"email": "test", "password": "1234"}
        self.bad_response = self.client.post(
            reverse("user_registration"),  # urls.urlpatterns name
            self.userprofile_bad_data,
            format="json",
        )

    def test_user_registration(self):
        """Test the api has bucket creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_invalid_user_registration(self):
        self.assertEqual(self.bad_response.status_code, status.HTTP_400_BAD_REQUEST)
