from django.urls import path

from .views import (
    JobListView,
    MyApplicationsView,
    RecruiterApplicationDetailView,
    RecruiterApplicationListView,
)

app_name = "jobs"

urlpatterns = [
    path("postings/", JobListView.as_view(), name="job-list"),
    path("applications/", MyApplicationsView.as_view(), name="my-applications"),
    path("recruiter/applications/", RecruiterApplicationListView.as_view(), name="recruiter-applications"),
    path("recruiter/applications/<uuid:pk>/", RecruiterApplicationDetailView.as_view(), name="recruiter-application-detail"),
]