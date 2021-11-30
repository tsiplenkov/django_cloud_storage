import io
import os

from PIL import Image

from cloud_storage.settings.test import MEDIA_ROOT

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from files.models import UserFile
from files.serializers import (
    UserFileSerializer,
    DownloadSerializer,
    PublicAccessSetterSerializer,
)
from users.models import UserProfile


def generate_text_file():
    if not os.path.isdir(MEDIA_ROOT):
        os.makedirs(MEDIA_ROOT)
    file_path = f"{MEDIA_ROOT}/test.txt"
    with open(file_path, "w") as file:
        file.write("Test text file\n")
    return file_path


def generate_image_file():
    file = io.BytesIO()
    image = Image.new("RGBA", size=(100, 100), color=(155, 0, 0))
    image.save(file, "png")
    file.name = "test.png"
    file.seek(0)
    return file


class UserFileModelsSerializersTestCase(APITestCase):
    """Test files.models & files.serializers"""

    def setUp(self):

        self.client = APIClient()
        self.userprofile_email = "test@test.ru"
        self.userprofile_data = {
            "email": self.userprofile_email,
            "password": "test1234",
        }
        # user registration
        self.reg_response = self.client.post(
            reverse("user_registration"),
            self.userprofile_data,
            format="json",
        )
        self.user_id = self.reg_response.data["user_id"]
        # user login
        self.auth_response = self.client.post(
            reverse("token_obtain_pair"),
            self.userprofile_data,
            format="json",
        )
        self.auth_token = self.auth_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.auth_token}")
        self.text_file = generate_text_file()
        self.user_file = UserFile(
            file_object=self.text_file,
            owner=UserProfile.objects.get(email=self.userprofile_email),
        )

    def test_create_remove_UserFile_model(self):
        """Test the userprofile model can create and remove a userprofile."""

        # create file
        old_count = UserFile.objects.count()
        self.user_file.save()
        new_count = UserFile.objects.count()
        self.assertNotEqual(old_count, new_count)
        self.assertTrue(os.path.isfile(self.user_file.file_object.path))

        # remove file
        old_count = UserFile.objects.count()
        self.user_file.delete()
        new_count = UserFile.objects.count()
        self.assertNotEqual(old_count, new_count)
        self.assertFalse(os.path.isfile(self.user_file.file_object.path))

    def test_UserFileSerializer(self):

        self.serializer = UserFileSerializer(instance=self.user_file)

        data = set(self.serializer.data)
        serializers_field = {
            "filename",
            "public_url",
            "created_time",
            "public_access",
            "file_url",
            "owner",
            "filesize",
            "file_id",
            "public_id",
        }
        self.assertEqual(data, serializers_field)

    def test_DownloadSerializer(self):
        self.serializer = DownloadSerializer(instance=self.user_file)

        data = set(self.serializer.data)
        serializers_field = {"file_object"}
        self.assertEqual(data, serializers_field)

    def test_PublicAccessSetterSerializer(self):
        self.serializer = PublicAccessSetterSerializer(instance=self.user_file)

        data = set(self.serializer.data)
        serializers_field = set()
        self.assertEqual(data, serializers_field)


class UserFileViewsTestCase(APITestCase):
    """Test files.views with auth
    UserFileListView ("files-list"): ["get /files", "post /files"]
    UserFileDetailView ("files-detail"): ["get /files/<file_id>", "post /files/<file_id>", "delete /files/<file_id>"]
    DownloadViewSet ("file-download"): ["get /files/<file_id>"/download"]
    PublicUserFileViewSet ("public-file-download"): ["get /public/<file_id>"]
    """

    def setUp(self):
        """Define the test client and other test variables."""
        # user registration
        self.client = APIClient()
        self.userprofile_email = "test@test.ru"
        self.userprofile_data = {
            "email": self.userprofile_email,
            "password": "test1234",
        }

        # user registration
        self.reg_response = self.client.post(
            reverse("user_registration"),
            self.userprofile_data,
            format="json",
        )
        self.user_id = self.reg_response.data["user_id"]

        # user login
        self.auth_response = self.client.post(
            reverse("token_obtain_pair"),
            self.userprofile_data,
            format="json",
        )
        self.auth_token = self.auth_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.auth_token}")
        self.image_file = generate_image_file()

        # post /files
        self.userprofile_data = {"file_object": self.image_file}
        self.post_files_response = self.client.post(
            reverse("files-list"),
            self.userprofile_data,
            format="multipart",
        )

        # get /files
        self.get_files_list_response = self.client.get(
            reverse("files-list"),
        )
        self.file_id = self.get_files_list_response.data[0]["file_id"]
        self.public_id = self.get_files_list_response.data[0]["public_id"]

        # get /files/<file_id>
        self.get_file_by_id_response = self.client.get(
            reverse("file-detail", kwargs={"file_id": self.file_id}),
        )

        # patch /files/<file_id>
        self.patch_file_by_id_response = self.client.patch(
            reverse("file-detail", kwargs={"file_id": self.file_id}),
            {"public_access": "True"},
        )

        # get /files/<file_id>/download
        self.download_file_by_id_response = self.client.get(
            reverse("file-download", kwargs={"file_id": self.file_id}),
        )

        # get /public/<file_id>/download
        self.client_without_auth = APIClient()
        self.download_file_by_public_id_response = self.client_without_auth.get(
            reverse("public-file-download", kwargs={"public_id": self.public_id}),
        )

    def test_post_UserFileListView(self):
        self.assertEqual(
            self.post_files_response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(
            self.post_files_response.data["filename"],
            "test.png",
        )

    def test_get_UserFileListView(self):
        self.assertEqual(
            self.get_files_list_response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            self.post_files_response.data["filename"],
            "test.png",
        )

    def test_get_UserFileDetailView(self):

        self.assertEqual(
            self.get_file_by_id_response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            self.get_file_by_id_response.data["owner"], self.userprofile_email
        )

    def test_patch_UserFileDetailView(self):
        self.assertEqual(
            self.patch_file_by_id_response.status_code,
            status.HTTP_200_OK,
        )
        self.assertTrue(self.patch_file_by_id_response.data["public_access"])

    def test_get_DownloadViewSet(self):
        self.assertEqual(
            self.download_file_by_id_response.status_code,
            status.HTTP_200_OK,
        )
        # self.assertEqual(self.download_file_by_id_response, self.image_file) #TODO: fix different objects

    def test_get_PublicDownloadViewSet(self):
        self.assertEqual(
            self.download_file_by_public_id_response.status_code,
            status.HTTP_200_OK,
        )
        # self.assertEqual(self.download_file_by_id_response, self.image_file) #TODO: fix different objects

    def test_delete_UserFileDetailView(self):
        # delete files/<file_id>
        self.delete_file_by_id_response = self.client.delete(
            reverse("file-detail", kwargs={"file_id": self.file_id}),
        )
        self.assertEqual(
            self.delete_file_by_id_response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.get_not_exist_file_by_id_response = self.client.get(
            reverse("file-detail", kwargs={"file_id": self.file_id}),
        )
        self.assertEqual(
            self.get_not_exist_file_by_id_response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
