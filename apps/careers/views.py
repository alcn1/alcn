from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions

from apps.candidates.models import CandidateProfile

from .models import CareerRoadmap, RoadmapMilestone, SkillAssessment
from .serializers import (
    CareerRoadmapSerializer,
    RoadmapMilestoneSerializer,
    SkillAssessmentSerializer,
)


class MyRoadmapView(generics.RetrieveUpdateAPIView):
    """GET/PATCH /api/careers/roadmap/ — the logged-in candidate's roadmap.
    Auto-creates one on first access."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CareerRoadmapSerializer

    def get_object(self):
        candidate_profile, _ = CandidateProfile.objects.get_or_create(user=self.request.user)
        roadmap, _ = CareerRoadmap.objects.get_or_create(
            candidate=candidate_profile,
            defaults={"title": f"{candidate_profile.target_role or 'My'} Career Roadmap"},
        )
        return roadmap


class MyMilestonesView(generics.ListCreateAPIView):
    """GET/POST /api/careers/milestones/ — list or add milestones to my roadmap."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RoadmapMilestoneSerializer

    def get_queryset(self):
        candidate_profile = CandidateProfile.objects.get(user=self.request.user)
        return RoadmapMilestone.objects.filter(roadmap__candidate=candidate_profile)

    def perform_create(self, serializer):
        candidate_profile, _ = CandidateProfile.objects.get_or_create(user=self.request.user)
        roadmap, _ = CareerRoadmap.objects.get_or_create(
            candidate=candidate_profile,
            defaults={"title": f"{candidate_profile.target_role or 'My'} Career Roadmap"},
        )
        serializer.save(roadmap=roadmap)


class MilestoneDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PATCH/DELETE /api/careers/milestones/<id>/ — update status, etc."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RoadmapMilestoneSerializer

    def get_queryset(self):
        candidate_profile = CandidateProfile.objects.get(user=self.request.user)
        return RoadmapMilestone.objects.filter(roadmap__candidate=candidate_profile)


class MyAssessmentsView(generics.ListCreateAPIView):
    """GET/POST /api/careers/assessments/ — my skill assessment history."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SkillAssessmentSerializer

    def get_queryset(self):
        candidate_profile = CandidateProfile.objects.get(user=self.request.user)
        return SkillAssessment.objects.filter(candidate=candidate_profile)

    def perform_create(self, serializer):
        candidate_profile, _ = CandidateProfile.objects.get_or_create(user=self.request.user)
        serializer.save(candidate=candidate_profile)