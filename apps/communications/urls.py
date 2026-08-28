from django.urls import path

from .views import ConversationRoomView, SendMessageView

app_name = "communications"

urlpatterns = [
    path("requests/<uuid:request_id>/room/", ConversationRoomView.as_view(), name="room"),
    path("requests/<uuid:request_id>/messages/", SendMessageView.as_view(), name="send-message"),
]