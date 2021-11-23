import os

from django.db import models
from django.conf import settings
import uuid

from django.dispatch import receiver

from users.models import UserProfile
from files.field_serializers.fileModelFieldSerializer import (
    ContentTypeRestrictedFileField,
)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<user_id>/<filename>
    return "{0}/{1}".format(instance.owner.user_id, filename)


FILE_TYPES = (
    ("f", "File"),
    ("d", "Directory"),
)


class UserFile(models.Model):

    file_id = models.UUIDField(default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    file_parent_id = models.ForeignKey(
        "self", blank=True, null=True, on_delete=models.CASCADE, default=None
    )
    file_object = ContentTypeRestrictedFileField(
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
    filename = models.CharField(max_length=255, default="0")
    filesize = models.PositiveIntegerField(default=1)
    created_time = models.DateTimeField(auto_now=True)
    access_link = models.CharField(max_length=8, null=True, default=None)

    def save(self, *args, **kwargs):
        self.filename = self.file_object.name
        self.filesize = self.file_object.size
        super(UserFile, self).save(*args, **kwargs)


@receiver(models.signals.post_delete, sender=UserFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `UserFile` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


class Meta:
    ordering = ("-created_time",)


def __str__(self):
    return self.name
