from django.contrib import admin

from .models import CareerRoadmap, RoadmapMilestone, SkillAssessment


class MilestoneInline(admin.TabularInline):
    model = RoadmapMilestone
    extra = 0


@admin.register(CareerRoadmap)
class CareerRoadmapAdmin(admin.ModelAdmin):
    list_display = ["title", "candidate", "created_at"]
    search_fields = ["title", "candidate__user__email"]
    inlines = [MilestoneInline]


@admin.register(SkillAssessment)
class SkillAssessmentAdmin(admin.ModelAdmin):
    list_display = ["assessment_name", "candidate", "score", "taken_at"]
    list_filter = ["assessment_name"]