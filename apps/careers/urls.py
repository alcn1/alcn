from django.urls import path

from .views import MilestoneDetailView, MyAssessmentsView, MyMilestonesView, MyRoadmapView

app_name = "careers"

urlpatterns = [
    path("roadmap/", MyRoadmapView.as_view(), name="my-roadmap"),
    path("milestones/", MyMilestonesView.as_view(), name="my-milestones"),
    path("milestones/<uuid:pk>/", MilestoneDetailView.as_view(), name="milestone-detail"),
    path("assessments/", MyAssessmentsView.as_view(), name="my-assessments"),
]