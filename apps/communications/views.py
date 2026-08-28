from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsStaffRole
from apps.candidates.models import CandidateProfile
from apps.services.models import ServiceRequest

from .models import ConversationRoom, Message
from .serializers import ConversationRoomSerializer, MessageSerializer


def _get_room_for_user(user, request_id):
    """Returns the conversation room for a request, enforcing access:
    candidates can only access rooms for their own requests; staff/admin can access any."""

    service_request = ServiceRequest.objects.get(id=request_id)

    if user.role not in ("staff", "admin"):
        candidate_profile = CandidateProfile.objects.get(user=user)
        if service_request.candidate_id != candidate_profile.id:
            raise PermissionDenied("You do not have access to this conversation.")

    room, _ = ConversationRoom.objects.get_or_create(service_request=service_request)
    return room


class ConversationRoomView(APIView):
    """GET /api/communications/requests/<request_id>/room/
    Returns the conversation for a service request, auto-creating it if needed.
    Internal notes are automatically hidden from candidates (see serializer)."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, request_id):
        room = _get_room_for_user(request.user, request_id)
        serializer = ConversationRoomSerializer(room, context={"request": request})
        return Response(serializer.data)


class SendMessageView(generics.CreateAPIView):
    """POST /api/communications/requests/<request_id>/messages/
    Candidates can only send regular messages. Staff/admin can also
    set is_internal_note=True — but we reject that flag from candidates
    even if they try to send it, rather than trusting the frontend."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        request_id = self.kwargs["request_id"]
        room = _get_room_for_user(self.request.user, request_id)

        is_internal_note = serializer.validated_data.get("is_internal_note", False)
        if is_internal_note and self.request.user.role not in ("staff", "admin"):
            raise PermissionDenied("Only staff can create internal notes.")

        serializer.save(room=room, sender=self.request.user)