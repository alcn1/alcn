import uuid

from django.conf import settings
from django.db import models


class CandidateProfile(models.Model):
    """One-to-one extension of User, holding all candidate-specific data.
    Only created for users with role='candidate'."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="candidate_profile",
    )

    # Education & experience
    education = models.TextField(blank=True, help_text="Degree, institution, year")
    skills = models.TextField(blank=True, help_text="Comma-separated or freeform")
    experience_years = models.PositiveIntegerField(default=0)
    experience_summary = models.TextField(blank=True)

    # Career target
    target_role = models.CharField(max_length=255, blank=True)
    career_goal = models.TextField(blank=True, help_text="What the candidate wants to achieve")

    # Document links (actual files uploaded via the Document model below,
    # these fields store the currently 'active' resume/portfolio for quick access)
    resume_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "candidates_profile"

    def __str__(self):
        return f"Profile: {self.user.email}"


class Document(models.Model):
    """Uploaded files: resume, portfolio PDF, certificates, etc."""

    class DocumentType(models.TextChoices):
        RESUME = "resume", "Resume"
        PORTFOLIO = "portfolio", "Portfolio"
        CERTIFICATE = "certificate", "Certificate"
        OTHER = "other", "Other"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    candidate = models.ForeignKey(
        CandidateProfile, on_delete=models.CASCADE, related_name="documents"
    )
    document_type = models.CharField(max_length=20, choices=DocumentType.choices)
    file = models.FileField(upload_to="candidate_documents/")
    original_filename = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "candidates_document"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.document_type} - {self.candidate.user.email}"