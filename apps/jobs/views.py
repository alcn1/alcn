from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from apps.accounts.permissions import IsRecruiter
from apps.candidates.models import CandidateProfile

from .models import ApplicationStatusHistory, EmployerProfile, JobApplication, JobPosting
from .serializers import JobApplicationSerializer, JobPostingSerializer, RecruiterApplicationSerializer


class JobListView(generics.ListAPIView):
    """GET /api/jobs/postings/ — public job board (any logged-in user), active jobs only."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = JobPostingSerializer
    queryset = JobPosting.objects.filter(is_active=True)


class MyApplicationsView(generics.ListCreateAPIView):
    """GET/POST /api/jobs/applications/ — candidate's own applications."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = JobApplicationSerializer

    def get_queryset(self):
        candidate_profile = CandidateProfile.objects.get(user=self.request.user)
        return JobApplication.objects.filter(candidate=candidate_profile)

    def perform_create(self, serializer):
        if self.request.user.role != "candidate":
            raise PermissionDenied("Only candidates can apply to jobs.")
        candidate_profile, _ = CandidateProfile.objects.get_or_create(user=self.request.user)
        serializer.save(candidate=candidate_profile, status="applied")


class RecruiterApplicationListView(generics.ListAPIView):
    """GET /api/jobs/recruiter/applications/ — recruiter sees applicants
    to their own job postings only, filterable by ?status=applied etc."""

    permission_classes = [IsRecruiter]
    serializer_class = RecruiterApplicationSerializer

    def get_queryset(self):
        employer_profile = EmployerProfile.objects.get(user=self.request.user)
        queryset = JobApplication.objects.filter(job__employer=employer_profile)
        status_filter = self.request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset


class RecruiterApplicationDetailView(generics.RetrieveUpdateAPIView):
    """GET/PATCH /api/jobs/recruiter/applications/<id>/
    Recruiter updates status; every change is logged automatically."""

    permission_classes = [IsRecruiter]
    serializer_class = RecruiterApplicationSerializer

    def get_queryset(self):
        employer_profile = EmployerProfile.objects.get(user=self.request.user)
        return JobApplication.objects.filter(job__employer=employer_profile)

    def perform_update(self, serializer):
        old_status = serializer.instance.status
        instance = serializer.save()
        if old_status != instance.status:
            ApplicationStatusHistory.objects.create(
                application=instance, old_status=old_status, new_status=instance.status,
                changed_by=self.request.user,
            )