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

class UserFile(models.Model):

    file_id = models.UUIDField(default=uuid.uuid4, editable=False)
    file_url = models.CharField(max_length=255)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
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
        max_upload_size=settings.FILE_UPLOAD_MAX_MEMORY_SIZE
    )
    filename = models.CharField(max_length=255, default="0")
    filesize = models.PositiveIntegerField(default=1)
    created_time = models.DateTimeField(auto_now=True)
    public_access = models.BooleanField(default=False)
    public_id = models.UUIDField(default=uuid.uuid4, editable=False)
    public_url = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        self.filename = self.file_object.name
        self.filesize = self.file_object.size
        self.file_url = f"/files/{self.file_id}"
        self.public_url = f"/public/{self.public_id}"
        super(UserFile, self).save(*args, **kwargs)

    def __str__(self):
        return self.filename


@receiver(models.signals.post_delete, sender=UserFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `UserFile` object is deleted.
    """
    if instance.file_object:
        if os.path.isfile(instance.file_object.path):
            os.remove(instance.file_object.path)
