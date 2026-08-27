import uuid

from django.conf import settings
from django.db import models


class CareerRoadmap(models.Model):
    """A candidate's overall career plan toward their target role."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    candidate = models.OneToOneField(
        "candidates.CandidateProfile",
        on_delete=models.CASCADE,
        related_name="roadmap",
    )
    title = models.CharField(max_length=255)
    summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "careers_roadmap"

    def __str__(self):
        return f"Roadmap: {self.title} ({self.candidate.user.email})"


class RoadmapMilestone(models.Model):
    """A single step within a roadmap, e.g. 'Complete React course'."""

    class Status(models.TextChoices):
        NOT_STARTED = "not_started", "Not Started"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    roadmap = models.ForeignKey(
        CareerRoadmap, on_delete=models.CASCADE, related_name="milestones"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NOT_STARTED)
    target_date = models.DateField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "careers_milestone"
        ordering = ["order"]

    def __str__(self):
        return f"{self.title} ({self.status})"


class SkillAssessment(models.Model):
    """Result of a skill/interest assessment taken by a candidate."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    candidate = models.ForeignKey(
        "candidates.CandidateProfile",
        on_delete=models.CASCADE,
        related_name="assessments",
    )
    assessment_name = models.CharField(max_length=255)
    score = models.PositiveIntegerField(null=True, blank=True)
    result_summary = models.TextField(blank=True)
    taken_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "careers_skill_assessment"
        ordering = ["-taken_at"]

    def __str__(self):
        return f"{self.assessment_name} - {self.candidate.user.email}"