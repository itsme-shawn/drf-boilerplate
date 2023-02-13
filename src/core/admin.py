"""
Django admin customization
"""

from django.contrib import admin
from django.contrib.auth.admin import (
    UserAdmin as BaseUserAdmin,
)  # 기존 UserAdmin 을 커스텀할 것이기 때문에 기존 UserAdmin 은 이름 바꿔줌
from django.utils.translation import gettext_lazy as _  # 번역

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users"""

    ordering = ["id"]
    list_display = ["email", "name"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal Info"), {"fields": ("name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    readonly_fields = ["last_login"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


admin.site.register(models.User, UserAdmin)  # 두 번째인자인 UserAdmin 은 선택이지만, 커스텀했기때문에 넣어줘야함
