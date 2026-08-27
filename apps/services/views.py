from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsStaffRole
from apps.candidates.models import CandidateProfile

from .models import RequestStatus, ServiceRequest, StatusHistory
from .serializers import ServiceRequestSerializer, StaffServiceRequestSerializer


class MyServiceRequestsView(generics.ListCreateAPIView):
    """GET/POST /api/services/requests/ — candidate's own service requests."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ServiceRequestSerializer

    def get_queryset(self):
        candidate_profile = CandidateProfile.objects.get(user=self.request.user)
        return ServiceRequest.objects.filter(candidate=candidate_profile)

    def perform_create(self, serializer):
        candidate_profile, _ = CandidateProfile.objects.get_or_create(user=self.request.user)
        serializer.save(candidate=candidate_profile, status=RequestStatus.NEW)


class MyServiceRequestDetailView(generics.RetrieveAPIView):
    """GET /api/services/requests/<id>/ — candidate viewing their own request."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ServiceRequestSerializer

    def get_queryset(self):
        candidate_profile = CandidateProfile.objects.get(user=self.request.user)
        return ServiceRequest.objects.filter(candidate=candidate_profile)


class StaffServiceRequestListView(generics.ListAPIView):
    """GET /api/services/staff/requests/ — staff/admin view of ALL requests,
    filterable by ?status=new etc."""

    permission_classes = [IsStaffRole]
    serializer_class = StaffServiceRequestSerializer

    def get_queryset(self):
        queryset = ServiceRequest.objects.all()
        status_filter = self.request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset


class StaffServiceRequestDetailView(generics.RetrieveUpdateAPIView):
    """GET/PATCH /api/services/staff/requests/<id>/ — staff can update status,
    notes, assigned_specialist. Every status change is logged automatically."""

    permission_classes = [IsStaffRole]
    serializer_class = StaffServiceRequestSerializer
    queryset = ServiceRequest.objects.all()

    def perform_update(self, serializer):
        old_status = serializer.instance.status
        instance = serializer.save()
        new_status = instance.status
        if old_status != new_status:
            StatusHistory.objects.create(
                request=instance,
                old_status=old_status,
                new_status=new_status,
                changed_by=self.request.user,
            )