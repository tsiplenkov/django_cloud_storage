from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import UserFile


# class FileModelAdmin(UserAdmin):
#     model = FileModel
#     list_display = (
#         "email",
#         "disk_space",
#         "used_space",
#     )
#     list_filter = (
#         "email",
#         "disk_space",
#         "used_space",
#     )
#     fieldsets = (
#         (None, {"fields": ("email", "password")}),
#         ("Permissions", {"fields": ("disk_space", "used_space")}),
#     )
#     add_fieldsets = (
#         (
#             None,
#             {
#                 "classes": ("wide",),
#                 "fields": ("email", "password1", "password2", "disk_space", "used_space"),
#             },
#         ),
#     )
#     search_fields = ("email",)
#     ordering = ("email",)


admin.site.register(UserFile)