from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UserProfileCreationForm, UserProfileChangeForm
from .models import UserProfile


class UserProfileAdmin(UserAdmin):
    add_form = UserProfileCreationForm
    form = UserProfileChangeForm
    model = UserProfile
    list_display = (
        "email",
        "disk_space",
        "used_space",
    )
    list_filter = (
        "email",
        "disk_space",
        "used_space",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("disk_space", "used_space")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "disk_space", "used_space"),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(UserProfile, UserProfileAdmin)
