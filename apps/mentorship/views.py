from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from apps.candidates.models import CandidateProfile

from .models import MentorProfile, Session
from .serializers import MentorProfileSerializer, MentorSessionUpdateSerializer, SessionSerializer

class MentorListView(generics.ListAPIView):
    """GET /api/mentorship/mentors/ — browse active mentors (any logged-in user)."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MentorProfileSerializer
    queryset = MentorProfile.objects.filter(is_active=True)


class MySessionsView(generics.ListCreateAPIView):
    """GET/POST /api/mentorship/sessions/
    Candidates: see/book their own sessions.
    Mentors: see sessions booked with them."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SessionSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == "mentor":
            return Session.objects.filter(mentor__user=user)
        return Session.objects.filter(candidate__user=user)

    def perform_create(self, serializer):
        if self.request.user.role != "candidate":
            raise PermissionDenied("Only candidates can book sessions.")
        candidate_profile, _ = CandidateProfile.objects.get_or_create(user=self.request.user)
        serializer.save(candidate=candidate_profile, status="requested")


class SessionDetailView(generics.RetrieveUpdateAPIView):
    """GET/PATCH /api/mentorship/sessions/<id>/
    Mentors can update status (confirm/complete/cancel) and add meeting_link.
    Candidates can only view."""

    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user.role == "mentor":
            return MentorSessionUpdateSerializer
        return SessionSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == "mentor":
            return Session.objects.filter(mentor__user=user)
        return Session.objects.filter(candidate__user=user)

    def perform_update(self, serializer):
        if self.request.user.role != "mentor":
            raise PermissionDenied("Only the mentor can update this session.")
        serializer.save()