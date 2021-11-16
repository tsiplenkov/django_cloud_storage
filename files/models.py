from django.db import models
from django.utils import timezone
from django.conf import settings
import uuid


from users.models import UserProfile
from files.field_serializers.fileModelFieldSerializer import ContentTypeRestrictedFileField


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<public_id>/<filename>
    return "user_{0}/{1}".format(instance.user.public_id, filename)


FILE_TYPES = (
    ("f", "File"),
    ("d", "Directory"),
)


class UserFile(models.Model):

    name = models.CharField(max_length=255)
    created_time = models.DateTimeField("date published", default=timezone.now)
    file_type = models.CharField(max_length=1, choices=FILE_TYPES)
    size = models.PositiveIntegerField(blank=False, null=False)
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    file_parent_id = models.ForeignKey("self", blank=True, on_delete=models.CASCADE)
    file_path = ContentTypeRestrictedFileField(
        upload_to=user_directory_path,
        verbose_name="File",
        content_types=[
            "image/jpeg",
            "application/pdf",
            "video/mp4",
            "audio/mpeg",
            "image/png",
        ],
        max_upload_size=settings.FILE_UPLOAD_MAX_MEMORY_SIZE,
    )
    access_link = models.CharField(max_length=8, default=(str(uuid.uuid4)[:8]))


class Meta:
    ordering = ("-created_time",)


def __str__(self):
    return self.name
