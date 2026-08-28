from rest_framework import serializers

from .models import ApplicationStatusHistory, EmployerProfile, JobApplication, JobPosting


class JobPostingSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="employer.company_name", read_only=True)

    class Meta:
        model = JobPosting
        fields = [
            "id", "title", "description", "location", "employment_type",
            "salary_min", "salary_max", "is_active", "company_name", "created_at",
        ]
        read_only_fields = ["id", "company_name", "created_at"]


class ApplicationStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationStatusHistory
        fields = ["id", "old_status", "new_status", "changed_at"]
        read_only_fields = fields


class JobApplicationSerializer(serializers.ModelSerializer):
    """Used by candidates: can apply and view, but not set status."""

    job_title = serializers.CharField(source="job.title", read_only=True)
    company_name = serializers.CharField(source="job.employer.company_name", read_only=True)
    status_history = ApplicationStatusHistorySerializer(many=True, read_only=True)

    class Meta:
        model = JobApplication
        fields = [
            "id", "job", "job_title", "company_name", "status",
            "cover_note", "status_history", "applied_at", "updated_at",
        ]
        read_only_fields = [
            "id", "job_title", "company_name", "status",
            "status_history", "applied_at", "updated_at",
        ]


class RecruiterApplicationSerializer(JobApplicationSerializer):
    """Used by recruiters: CAN update status."""

    candidate_email = serializers.EmailField(source="candidate.user.email", read_only=True)

    class Meta(JobApplicationSerializer.Meta):
        fields = JobApplicationSerializer.Meta.fields + ["candidate_email"]
        read_only_fields = [
            "id", "job_title", "company_name", "candidate_email",
            "status_history", "applied_at", "updated_at",
        ]