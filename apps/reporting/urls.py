from django.urls import path

from .views import DashboardMetricsView

app_name = "reporting"

urlpatterns = [
    path("dashboard/", DashboardMetricsView.as_view(), name="dashboard"),
]