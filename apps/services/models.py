import uuid

from django.conf import settings
from django.db import models


class ServiceType(models.TextChoices):
    ATS_RESUME = "ats_resume", "ATS Resume"
    LINKEDIN_OPTIMIZATION = "linkedin_optimization", "LinkedIn Optimization"
    NAUKRI_PROFILE = "naukri_profile", "Naukri Profile"
    PORTFOLIO = "portfolio", "Portfolio"
    CAREER_GUIDANCE = "career_guidance", "Career Guidance"
    MOCK_INTERVIEW = "mock_interview", "Mock Interview"


class RequestStatus(models.TextChoices):
    NEW = "new", "New"
    UNDER_REVIEW = "under_review", "Under Review"
    ACCEPTED = "accepted", "Accepted for Consultation"
    IN_PROGRESS = "in_progress", "In Progress"
    COMPLETED = "completed", "Completed"
    DECLINED = "declined", "Declined"


class ServiceRequest(models.Model):
    """A candidate's request for one of the ALCN Career services."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    candidate = models.ForeignKey(
        "candidates.CandidateProfile",
        on_delete=models.CASCADE,
        related_name="service_requests",
    )
    service_type = models.CharField(max_length=30, choices=ServiceType.choices)
    notes = models.TextField(blank=True, help_text="Candidate's notes/requirements")
    status = models.CharField(max_length=20, choices=RequestStatus.choices, default=RequestStatus.NEW)

    assigned_specialist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_requests",
        limit_choices_to={"role__in": ["staff", "admin"]},
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "services_request"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_service_type_display()} - {self.candidate.user.email} [{self.status}]"


class RequestAttachment(models.Model):
    """Files attached to a service request (by candidate or staff)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    request = models.ForeignKey(
        ServiceRequest, on_delete=models.CASCADE, related_name="attachments"
    )
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to="request_attachments/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "services_request_attachment"
        ordering = ["-uploaded_at"]


class StatusHistory(models.Model):
    """Audit trail: every status change on a request, who made it, and when."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    request = models.ForeignKey(
        ServiceRequest, on_delete=models.CASCADE, related_name="status_history"
    )
    old_status = models.CharField(max_length=20, choices=RequestStatus.choices, blank=True)
    new_status = models.CharField(max_length=20, choices=RequestStatus.choices)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    note = models.TextField(blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "services_status_history"
        ordering = ["-changed_at"]

    def __str__(self):
        return f"{self.old_status} -> {self.new_status}"