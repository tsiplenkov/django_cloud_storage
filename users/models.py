import os
from django.conf import settings

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import UserProfileManager
import uuid


class UserProfile(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(_("email address"), unique=True)
    disk_space = models.PositiveIntegerField(default=1024 ** 3, blank=False, null=False)
    used_space = models.IntegerField(default=0, blank=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserProfileManager()

    def __str__(self):
        return self.email

@receiver(models.signals.post_save, sender=UserProfile)
def auto_create_user_dir_on_create(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `UserFile` object is deleted.
    """
    user_dir = f"{settings.MEDIA_ROOT}/{instance.user_id}"
    if not os.path.isdir(user_dir):
        os.makedirs(user_dir)

@receiver(models.signals.post_delete, sender=UserProfile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `UserFile` object is deleted.
    """
    user_dir = f"{settings.MEDIA_ROOT}/{instance.user_id}"
    if os.path.isdir(user_dir):
        os.rmdir(user_dir)
