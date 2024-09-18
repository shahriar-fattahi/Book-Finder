from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminChangeForm, UserAdminCreationForm
from .models import User


class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ["username", "id"]
    list_filter = ["is_superuser"]

    fieldsets = [
        ("Identifire", {"fields": ["username"]}),
        (
            "Personal Information",
            {
                "fields": [
                    "password",
                ],
            },
        ),
        (
            "Permissions",
            {
                "fields": [
                    "is_superuser",
                ],
            },
        ),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "username",
                    "password",
                    "password_confirm",
                ],
            },
        ),
    ]
    search_fields = ["username"]
    ordering = ["id"]
    filter_horizontal = []


admin.site.register(User, UserAdmin)
