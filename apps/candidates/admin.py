from django.contrib import admin

from .models import CandidateProfile, Document


class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0
    readonly_fields = ["uploaded_at"]


@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "target_role", "experience_years", "updated_at"]
    search_fields = ["user__email", "user__first_name", "user__last_name", "target_role"]
    readonly_fields = ["id", "created_at", "updated_at"]
    inlines = [DocumentInline]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["candidate", "document_type", "uploaded_at"]
    list_filter = ["document_type"]