from django.contrib import admin

from .models import ConversationRoom, MeetingRecord, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ["sender", "sent_at"]


class MeetingInline(admin.TabularInline):
    model = MeetingRecord
    extra = 0
    readonly_fields = ["scheduled_by", "created_at"]


@admin.register(ConversationRoom)
class ConversationRoomAdmin(admin.ModelAdmin):
    list_display = ["service_request", "created_at"]
    inlines = [MessageInline, MeetingInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["room", "sender", "is_internal_note", "sent_at"]
    list_filter = ["is_internal_note"]