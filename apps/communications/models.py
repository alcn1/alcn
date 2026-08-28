import uuid

from django.conf import settings
from django.db import models


class ConversationRoom(models.Model):
    """One conversation thread, tied to a specific service request."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service_request = models.OneToOneField(
        "services.ServiceRequest",
        on_delete=models.CASCADE,
        related_name="conversation",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "communications_room"

    def __str__(self):
        return f"Room for request {self.service_request_id}"


class Message(models.Model):
    """A single chat message within a conversation room."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(ConversationRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    text = models.TextField(blank=True)
    file = models.FileField(upload_to="message_attachments/", null=True, blank=True)
    is_internal_note = models.BooleanField(
        default=False,
        help_text="If True, only visible to staff/admin — hidden from the candidate.",
    )
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "communications_message"
        ordering = ["sent_at"]

    def __str__(self):
        return f"{self.sender}: {self.text[:40]}"


class MeetingRecord(models.Model):
    """Record of a scheduled call/screen-share session for a conversation."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(ConversationRoom, on_delete=models.CASCADE, related_name="meetings")
    scheduled_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    meeting_link = models.URLField(help_text="Jitsi/LiveKit/Google Meet/Teams link")
    scheduled_at = models.DateTimeField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "communications_meeting"
        ordering = ["-scheduled_at"]

    def __str__(self):
        return f"Meeting at {self.scheduled_at}"