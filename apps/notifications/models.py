import uuid

from django.conf import settings
from django.db import models


class NotificationType(models.TextChoices):
    SERVICE_REQUEST_UPDATE = "service_request_update", "Service Request Update"
    NEW_MESSAGE = "new_message", "New Message"
    SESSION_UPDATE = "session_update", "Session Update"
    APPLICATION_UPDATE = "application_update", "Application Update"
    GENERAL = "general", "General"


class Notification(models.Model):
    """An in-app notification for a user. Also the record of what would be
    emailed out — email sending itself is handled by Celery tasks that read
    from this table (wired up in the Integration phase)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    notification_type = models.CharField(max_length=30, choices=NotificationType.choices, default=NotificationType.GENERAL)
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    link = models.CharField(max_length=500, blank=True, help_text="Frontend route to navigate to, e.g. /requests/123")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notifications_notification"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.notification_type} -> {self.user.email}"