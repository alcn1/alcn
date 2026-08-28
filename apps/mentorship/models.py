import uuid

from django.conf import settings
from django.db import models


class MentorProfile(models.Model):
    """Profile for a user with role='mentor'."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="mentor_profile",
        limit_choices_to={"role": "mentor"},
    )
    bio = models.TextField(blank=True)
    expertise = models.CharField(max_length=255, blank=True, help_text="e.g. Frontend, Data Science, Product")
    years_experience = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "mentorship_mentor_profile"

    def __str__(self):
        return f"Mentor: {self.user.email}"


class Availability(models.Model):
    """A recurring or one-off time slot a mentor is available."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE, related_name="availability_slots")
    day_of_week = models.PositiveSmallIntegerField(
        choices=[(0, "Monday"), (1, "Tuesday"), (2, "Wednesday"), (3, "Thursday"),
                 (4, "Friday"), (5, "Saturday"), (6, "Sunday")],
    )
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        db_table = "mentorship_availability"

    def __str__(self):
        return f"{self.mentor} - {self.get_day_of_week_display()} {self.start_time}-{self.end_time}"


class SessionType(models.TextChoices):
    MENTORSHIP = "mentorship", "Mentorship Session"
    MOCK_INTERVIEW = "mock_interview", "Mock Interview"


class SessionStatus(models.TextChoices):
    REQUESTED = "requested", "Requested"
    CONFIRMED = "confirmed", "Confirmed"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"


class Session(models.Model):
    """A booked session between a candidate and a mentor."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE, related_name="sessions")
    candidate = models.ForeignKey(
        "candidates.CandidateProfile", on_delete=models.CASCADE, related_name="mentor_sessions"
    )
    service_request = models.ForeignKey(
        "services.ServiceRequest",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mentor_sessions",
        help_text="Optional link if this session was booked via a Mock Interview service request",
    )
    session_type = models.CharField(max_length=20, choices=SessionType.choices)
    status = models.CharField(max_length=20, choices=SessionStatus.choices, default=SessionStatus.REQUESTED)
    scheduled_at = models.DateTimeField()
    meeting_link = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "mentorship_session"
        ordering = ["-scheduled_at"]

    def __str__(self):
        return f"{self.session_type} - {self.candidate.user.email} with {self.mentor.user.email}"


class SessionFeedback(models.Model):
    """Feedback left after a session — either party can leave feedback."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.OneToOneField(Session, on_delete=models.CASCADE, related_name="feedback")
    rating = models.PositiveSmallIntegerField(help_text="1-5")
    comments = models.TextField(blank=True)
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "mentorship_session_feedback"

    def __str__(self):
        return f"Feedback for {self.session_id}: {self.rating}/5"