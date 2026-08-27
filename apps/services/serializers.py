from rest_framework import serializers

from .models import RequestAttachment, ServiceRequest, StatusHistory


class RequestAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestAttachment
        fields = ["id", "file", "uploaded_by", "uploaded_at"]
        read_only_fields = ["id", "uploaded_by", "uploaded_at"]


class StatusHistorySerializer(serializers.ModelSerializer):
    changed_by_email = serializers.EmailField(source="changed_by.email", read_only=True)

    class Meta:
        model = StatusHistory
        fields = ["id", "old_status", "new_status", "changed_by_email", "note", "changed_at"]
        read_only_fields = fields


class ServiceRequestSerializer(serializers.ModelSerializer):
    """Used by candidates: can create/view their own requests, but cannot
    directly set status or assigned_specialist — those are staff-only actions."""

    attachments = RequestAttachmentSerializer(many=True, read_only=True)
    status_history = StatusHistorySerializer(many=True, read_only=True)
    candidate_email = serializers.EmailField(source="candidate.user.email", read_only=True)
    assigned_specialist_email = serializers.EmailField(
        source="assigned_specialist.email", read_only=True, allow_null=True
    )

    class Meta:
        model = ServiceRequest
        fields = [
            "id", "candidate_email", "service_type", "notes", "status",
            "assigned_specialist_email", "attachments", "status_history",
            "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "candidate_email", "status", "assigned_specialist_email",
            "attachments", "status_history", "created_at", "updated_at",
        ]


class StaffServiceRequestSerializer(ServiceRequestSerializer):
    """Used by staff/admin: CAN update status and assigned_specialist."""

    class Meta(ServiceRequestSerializer.Meta):
        read_only_fields = [
            "id", "candidate_email", "attachments", "status_history",
            "created_at", "updated_at",
        ]