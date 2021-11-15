from django.db import models

from users.models import UserProfile


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
    parrend_id = models.ForeignKey('self', blank=True)
    access_link =