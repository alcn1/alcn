from django.utils import timezone
from datetime import timedelta

from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import User
from apps.accounts.permissions import IsStaffRole
from apps.jobs.models import JobApplication
from apps.services.models import RequestStatus, ServiceRequest


class DashboardMetricsView(APIView):
    """GET /api/reporting/dashboard/ — staff/admin overview metrics.
    Matches your spec: registrations, service conversion, completion, placement rate."""

    permission_classes = [IsStaffRole]

    def get(self, request):
        thirty_days_ago = timezone.now() - timedelta(days=30)

        total_candidates = User.objects.filter(role="candidate").count()
        new_candidates_30d = User.objects.filter(role="candidate", date_joined__gte=thirty_days_ago).count()

        total_requests = ServiceRequest.objects.count()
        requests_by_status = {
            status_choice.value: ServiceRequest.objects.filter(status=status_choice.value).count()
            for status_choice in RequestStatus
        }

        completed_requests = requests_by_status.get("completed", 0)
        service_conversion_rate = (
            round((completed_requests / total_requests) * 100, 1) if total_requests else 0
        )

        total_applications = JobApplication.objects.count()
        hired_count = JobApplication.objects.filter(status="hired").count()
        placement_rate = (
            round((hired_count / total_applications) * 100, 1) if total_applications else 0
        )

        return Response({
            "candidates": {
                "total": total_candidates,
                "new_last_30_days": new_candidates_30d,
            },
            "service_requests": {
                "total": total_requests,
                "by_status": requests_by_status,
                "conversion_rate_percent": service_conversion_rate,
            },
            "job_applications": {
                "total": total_applications,
                "hired": hired_count,
                "placement_rate_percent": placement_rate,
            },
        })