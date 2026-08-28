from rest_framework import serializers

from .models import ConversationRoom, MeetingRecord, Message


class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.EmailField(source="sender.email", read_only=True)
    sender_role = serializers.CharField(source="sender.role", read_only=True)

    class Meta:
        model = Message
        fields = ["id", "sender_email", "sender_role", "text", "file", "is_internal_note", "sent_at"]
        read_only_fields = ["id", "sender_email", "sender_role", "sent_at"]


class MeetingRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRecord
        fields = ["id", "meeting_link", "scheduled_at", "notes", "created_at"]
        read_only_fields = ["id", "created_at"]


class ConversationRoomSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()
    meetings = MeetingRecordSerializer(many=True, read_only=True)

    class Meta:
        model = ConversationRoom
        fields = ["id", "service_request", "messages", "meetings", "created_at"]
        read_only_fields = fields

    def get_messages(self, obj):
        """Candidates never see internal notes. Staff/admin see everything."""
        request = self.context["request"]
        messages = obj.messages.all()
        if request.user.role not in ("staff", "admin"):
            messages = messages.filter(is_internal_note=False)
        return MessageSerializer(messages, many=True).data