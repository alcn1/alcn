from django.urls import path

from .views import MentorListView, MySessionsView, SessionDetailView

app_name = "mentorship"

urlpatterns = [
    path("mentors/", MentorListView.as_view(), name="mentor-list"),
    path("sessions/", MySessionsView.as_view(), name="my-sessions"),
    path("sessions/<uuid:pk>/", SessionDetailView.as_view(), name="session-detail"),
]