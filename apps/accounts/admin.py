from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import EmailVerificationToken, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    ordering = ["-date_joined"]
    list_display = ["email", "full_name", "role", "is_email_verified", "is_active", "date_joined"]
    list_filter = ["role", "is_active", "is_email_verified"]
    search_fields = ["email", "first_name", "last_name", "phone"]
    readonly_fields = ["id", "date_joined"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "phone")}),
        ("Role & status", {"fields": ("role", "is_active", "is_staff", "is_superuser", "is_email_verified")}),
        ("Important dates", {"fields": ("date_joined",)}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "role", "password1", "password2"),
        }),
    )
    filter_horizontal = ("groups", "user_permissions")


admin.site.register(EmailVerificationToken)