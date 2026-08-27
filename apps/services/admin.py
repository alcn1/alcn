from django.contrib import admin
from django.utils import timezone

from .models import RequestAttachment, ServiceRequest, StatusHistory


class AttachmentInline(admin.TabularInline):
    model = RequestAttachment
    extra = 0
    readonly_fields = ["uploaded_by", "uploaded_at"]


class StatusHistoryInline(admin.TabularInline):
    model = StatusHistory
    extra = 0
    readonly_fields = ["old_status", "new_status", "changed_by", "note", "changed_at"]
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


def _change_status(modeladmin, request, queryset, new_status):
    for service_request in queryset:
        old_status = service_request.status
        if old_status == new_status:
            continue
        service_request.status = new_status
        service_request.save(update_fields=["status", "updated_at"])
        StatusHistory.objects.create(
            request=service_request,
            old_status=old_status,
            new_status=new_status,
            changed_by=request.user,
        )
    modeladmin.message_user(request, f"Updated {queryset.count()} request(s) to '{new_status}'.")


@admin.action(description="Accept for consultation")
def accept_requests(modeladmin, request, queryset):
    _change_status(modeladmin, request, queryset, "accepted")


@admin.action(description="Mark as under review")
def mark_under_review(modeladmin, request, queryset):
    _change_status(modeladmin, request, queryset, "under_review")


@admin.action(description="Mark as in progress")
def mark_in_progress(modeladmin, request, queryset):
    _change_status(modeladmin, request, queryset, "in_progress")


@admin.action(description="Mark as completed")
def mark_completed(modeladmin, request, queryset):
    _change_status(modeladmin, request, queryset, "completed")


@admin.action(description="Decline request")
def decline_requests(modeladmin, request, queryset):
    _change_status(modeladmin, request, queryset, "declined")


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ["candidate", "service_type", "status", "assigned_specialist", "created_at"]
    list_filter = ["status", "service_type"]
    search_fields = ["candidate__user__email", "notes"]
    readonly_fields = ["id", "created_at", "updated_at"]
    inlines = [AttachmentInline, StatusHistoryInline]
    actions = [accept_requests, mark_under_review, mark_in_progress, mark_completed, decline_requests]