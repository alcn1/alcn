from django.urls import path

from .views import MarkNotificationReadView, MyNotificationsView

app_name = "notifications"

urlpatterns = [
    path("", MyNotificationsView.as_view(), name="my-notifications"),
    path("<uuid:pk>/read/", MarkNotificationReadView.as_view(), name="mark-read"),
]