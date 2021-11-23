from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import UserProfileManager
import uuid


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    disk_space = models.PositiveIntegerField(default=1024 ** 3, blank=False, null=False)
    used_space = models.IntegerField(default=0, blank=False)
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserProfileManager()

    def __str__(self):
        return self.email
