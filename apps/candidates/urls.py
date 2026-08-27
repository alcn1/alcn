from django.urls import path

from .views import MyCandidateProfileView

app_name = "candidates"

urlpatterns = [
    path("me/", MyCandidateProfileView.as_view(), name="my-profile"),
]