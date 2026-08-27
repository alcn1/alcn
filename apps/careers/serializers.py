from rest_framework import serializers

from .models import CareerRoadmap, RoadmapMilestone, SkillAssessment


class RoadmapMilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadmapMilestone
        fields = ["id", "title", "description", "order", "status", "target_date", "completed_at"]
        read_only_fields = ["id", "completed_at"]


class CareerRoadmapSerializer(serializers.ModelSerializer):
    milestones = RoadmapMilestoneSerializer(many=True, read_only=True)

    class Meta:
        model = CareerRoadmap
        fields = ["id", "title", "summary", "milestones", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class SkillAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillAssessment
        fields = ["id", "assessment_name", "score", "result_summary", "taken_at"]
        read_only_fields = ["id", "taken_at"]