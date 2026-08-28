from django.contrib import admin

from .models import Availability, MentorProfile, Session, SessionFeedback


class AvailabilityInline(admin.TabularInline):
    model = Availability
    extra = 0


@admin.register(MentorProfile)
class MentorProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "expertise", "years_experience", "is_active"]
    search_fields = ["user__email", "expertise"]
    inlines = [AvailabilityInline]


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ["candidate", "mentor", "session_type", "status", "scheduled_at"]
    list_filter = ["session_type", "status"]
    search_fields = ["candidate__user__email", "mentor__user__email"]


@admin.register(SessionFeedback)
class SessionFeedbackAdmin(admin.ModelAdmin):
    list_display = ["session", "rating", "submitted_at"]