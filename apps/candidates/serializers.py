from rest_framework import serializers

from .models import CandidateProfile, Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "document_type", "file", "original_filename", "uploaded_at"]
        read_only_fields = ["id", "uploaded_at"]


class CandidateProfileSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    full_name = serializers.CharField(source="user.full_name", read_only=True)

    class Meta:
        model = CandidateProfile
        fields = [
            "id", "email", "full_name",
            "education", "skills", "experience_years", "experience_summary",
            "target_role", "career_goal",
            "resume_url", "portfolio_url", "linkedin_url",
            "documents", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "email", "full_name", "documents", "created_at", "updated_at"]