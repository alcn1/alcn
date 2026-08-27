from rest_framework import generics, permissions

from .models import CandidateProfile
from .serializers import CandidateProfileSerializer


class MyCandidateProfileView(generics.RetrieveUpdateAPIView):
    """GET/PATCH /api/candidates/me/ — the logged-in candidate's own profile.
    Creates an empty profile automatically on first access if one doesn't exist yet."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CandidateProfileSerializer

    def get_object(self):
        profile, _ = CandidateProfile.objects.get_or_create(user=self.request.user)
        return profile