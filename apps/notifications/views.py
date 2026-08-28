from rest_framework import generics, permissions

from .models import Notification
from .serializers import NotificationSerializer


class MyNotificationsView(generics.ListAPIView):
    """GET /api/notifications/?is_read=false — the logged-in user's notifications."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        queryset = Notification.objects.filter(user=self.request.user)
        is_read = self.request.query_params.get("is_read")
        if is_read is not None:
            queryset = queryset.filter(is_read=(is_read.lower() == "true"))
        return queryset


class MarkNotificationReadView(generics.UpdateAPIView):
    """PATCH /api/notifications/<id>/read/ — mark one notification as read."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(is_read=True)