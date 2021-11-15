from django.db import models

import uuid

from users.models import UserProfile

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.public_id, filename)

class Question(models.Model):
    FILE_TYPES = (
        ('f', 'File'),
        ('d', 'Directory'),
    )
    name = models.CharField(max_length=255)
    created_time = models.DateTimeField('date published')
    file_type = models.CharField(max_length=1, choices=FILE_TYPES)
    size = models.PositiveIntegerField(blank=False, null=False)
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    file_parent_id = models.ForeignKey('self', blank=True)
    file = models.FileField(upload_to=user_directory_path,
                                  verbose_name='File', )
    access_link = models.CharField(default=str(uuid.uuid4())[:8])
