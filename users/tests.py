from django.test import override_settings
from django.urls import reverse

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from django.conf import settings
import os

# Create your tests here.
from .models import UserProfile
from .serializers import UserProfileSerializer


class ModelUserProfileTestCase(APITestCase):
    """This class defines the test suite for the userprofile model."""

    @override_settings(DJANGO_SETTINGS_MODULE="cloud_storage.settings.test")
    def setUp(self):
        """Define the test client and other test variables."""
        self.userprofile_email = "test@test.ru"
        self.userprofile_password = "test1234"
        self.userprofile = UserProfile(
            email=self.userprofile_email, password=self.userprofile_password
        )
        self.user_dir = f"{settings.MEDIA_ROOT}/{self.userprofile.user_id}"
        self.userprofile_id = self.userprofile.user_id

    @override_settings(DJANGO_SETTINGS_MODULE="cloud_storage.settings.test")
    def test_create_remove_userprofile_model(self):
        """Test the userprofile model can create and remove a userprofile."""

        # create user
        old_count = UserProfile.objects.count()
        self.userprofile.save()
        new_count = UserProfile.objects.count()
        self.assertNotEqual(old_count, new_count)
        # create user dir
        self.assertTrue(os.path.isdir(self.user_dir))

        # remove user
        old_count = UserProfile.objects.count()
        self.userprofile = UserProfile.objects.get(user_id=self.userprofile_id)
        self.userprofile.delete()
        new_count = UserProfile.objects.count()
        self.assertNotEqual(old_count, new_count)
        # remove user dir
        self.assertFalse(os.path.isdir(self.user_dir))


class SerializerUserProfileTestCase(APITestCase):
    @override_settings(DJANGO_SETTINGS_MODULE="cloud_storage.settings.test")
    def setUp(self):
        self.userprofile_attributes = {"email": "test@test.com", "password": "test123"}

        self.userprofile = UserProfile.objects.create(**self.userprofile_attributes)
        self.serializer = UserProfileSerializer(instance=self.userprofile)

    def test_contains_expected_fields(self):
        data = set(self.serializer.data)

        self.assertEqual(data, {"user_id", "email", "disk_space", "used_space"})


class SelfUserProfileDetailTestCase(APITestCase):
    """Test suite for SelfUserProfileDetail views."""

    @override_settings(DJANGO_SETTINGS_MODULE="cloud_storage.settings.test")
    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.userprofile_data = {"email": "test@test.ru", "password": "test1234"}
        # user registration
        self.reg_response = self.client.post(
            reverse("user_registration"),  # urls.urlpatterns name
            self.userprofile_data,
            format="json",
        )
        self.user_id = self.reg_response.data["user_id"]
        # user login
        self.auth_response = self.client.post(
            reverse("token_obtain_pair"),  # urls.urlpatterns name
            self.userprofile_data,
            format="json",
        )
        self.auth_token = self.auth_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.auth_token}")

    @override_settings(DJANGO_SETTINGS_MODULE="cloud_storage.settings.test")
    def test_get_user_profile_detail(self):
        """Test the api has bucket creation capability."""
        self.get_response = self.client.get(reverse("userself-detail"))
        self.assertEqual(self.get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.get_response.data["email"], self.userprofile_data["email"]
        )

    @override_settings(DJANGO_SETTINGS_MODULE="cloud_storage.settings.test")
    def test_patch_user_profile_detail(self):
        self.new_userprofile_data = {"password": "test12345"}
        self.patch_response = self.client.patch(
            reverse("userself-detail"),  # urls.urlpatterns name
            self.new_userprofile_data,
            format="json",
        )

        self.assertEqual(self.patch_response.status_code, status.HTTP_200_OK)

        self.auth_response = self.client.post(
            reverse("token_obtain_pair"),  # urls.urlpatterns name
            {"email": "test@test.com", "password": "test12345"},
            format="json",
        )
        self.assertEqual(self.patch_response.status_code, status.HTTP_200_OK)

    @override_settings(DJANGO_SETTINGS_MODULE="cloud_storage.settings.test")
    def test_delete_user_profile_detail(self):
        self.patch_response = self.client.delete(
            reverse("userself-detail"),  # urls.urlpatterns name
            format="json",
        )

        self.assertEqual(self.patch_response.status_code, status.HTTP_204_NO_CONTENT)
