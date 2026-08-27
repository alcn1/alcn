from django.urls import path

from .views import (
    MyServiceRequestDetailView,
    MyServiceRequestsView,
    StaffServiceRequestDetailView,
    StaffServiceRequestListView,
)

app_name = "services"

urlpatterns = [
    path("requests/", MyServiceRequestsView.as_view(), name="my-requests"),
    path("requests/<uuid:pk>/", MyServiceRequestDetailView.as_view(), name="my-request-detail"),
    path("staff/requests/", StaffServiceRequestListView.as_view(), name="staff-requests"),
    path("staff/requests/<uuid:pk>/", StaffServiceRequestDetailView.as_view(), name="staff-request-detail"),
]