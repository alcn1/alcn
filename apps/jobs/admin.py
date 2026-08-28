from django.contrib import admin

from .models import ApplicationStatusHistory, EmployerProfile, JobApplication, JobPosting


class JobPostingInline(admin.TabularInline):
    model = JobPosting
    extra = 0


@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ["company_name", "user", "is_verified"]
    search_fields = ["company_name", "user__email"]
    inlines = [JobPostingInline]


class StatusHistoryInline(admin.TabularInline):
    model = ApplicationStatusHistory
    extra = 0
    readonly_fields = ["old_status", "new_status", "changed_by", "changed_at"]
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


def _change_application_status(modeladmin, request, queryset, new_status):
    for application in queryset:
        old_status = application.status
        if old_status == new_status:
            continue
        application.status = new_status
        application.save(update_fields=["status", "updated_at"])
        ApplicationStatusHistory.objects.create(
            application=application, old_status=old_status, new_status=new_status, changed_by=request.user
        )
    modeladmin.message_user(request, f"Updated {queryset.count()} application(s) to '{new_status}'.")


@admin.action(description="Mark as Screened")
def mark_screened(modeladmin, request, queryset):
    _change_application_status(modeladmin, request, queryset, "screened")


@admin.action(description="Mark as Shortlisted")
def mark_shortlisted(modeladmin, request, queryset):
    _change_application_status(modeladmin, request, queryset, "shortlisted")


@admin.action(description="Mark as Interview")
def mark_interview(modeladmin, request, queryset):
    _change_application_status(modeladmin, request, queryset, "interview")


@admin.action(description="Mark as Offer")
def mark_offer(modeladmin, request, queryset):
    _change_application_status(modeladmin, request, queryset, "offer")


@admin.action(description="Mark as Hired")
def mark_hired(modeladmin, request, queryset):
    _change_application_status(modeladmin, request, queryset, "hired")


@admin.action(description="Mark as Rejected")
def mark_rejected(modeladmin, request, queryset):
    _change_application_status(modeladmin, request, queryset, "rejected")


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ["title", "employer", "employment_type", "is_active", "created_at"]
    list_filter = ["employment_type", "is_active"]
    search_fields = ["title", "employer__company_name"]


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ["candidate", "job", "status", "applied_at"]
    list_filter = ["status"]
    search_fields = ["candidate__user__email", "job__title"]
    inlines = [StatusHistoryInline]
    actions = [mark_screened, mark_shortlisted, mark_interview, mark_offer, mark_hired, mark_rejected]