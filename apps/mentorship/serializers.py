from rest_framework import serializers

from .models import Availability, MentorProfile, Session, SessionFeedback


class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ["id", "day_of_week", "start_time", "end_time"]


class MentorProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    full_name = serializers.CharField(source="user.full_name", read_only=True)
    availability_slots = AvailabilitySerializer(many=True, read_only=True)

    class Meta:
        model = MentorProfile
        fields = [
            "id", "email", "full_name", "bio", "expertise",
            "years_experience", "is_active", "availability_slots",
        ]


class SessionFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionFeedback
        fields = ["id", "rating", "comments", "submitted_at"]
        read_only_fields = ["id", "submitted_at"]


class SessionSerializer(serializers.ModelSerializer):
    """Used by candidates: can view/book, but status is read-only for them."""

    mentor_email = serializers.EmailField(source="mentor.user.email", read_only=True)
    candidate_email = serializers.EmailField(source="candidate.user.email", read_only=True)
    feedback = SessionFeedbackSerializer(read_only=True)

    class Meta:
        model = Session
        fields = [
            "id", "mentor", "mentor_email", "candidate_email", "service_request",
            "session_type", "status", "scheduled_at", "meeting_link",
            "feedback", "created_at",
        ]
        read_only_fields = [
            "id", "mentor_email", "candidate_email", "status",
            "feedback", "created_at",
        ]


class MentorSessionUpdateSerializer(SessionSerializer):
    """Used by mentors: CAN update status and meeting_link."""

    class Meta(SessionSerializer.Meta):
        read_only_fields = [
            "id", "mentor_email", "candidate_email",
            "feedback", "created_at",
        ]