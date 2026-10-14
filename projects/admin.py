from django.contrib import admin

from .models import (
    Alignment,
    Comment,
    Contact,
    DTContact,
    DeveloperAPIKey,
    Keyword,
    Status,
    Task,
    Tracker,
    Update,
)

admin.site.register(Tracker)
admin.site.register(Task)
admin.site.register(Contact)
admin.site.register(Status)
admin.site.register(Keyword)
admin.site.register(Update)
admin.site.register(Alignment)
admin.site.register(Comment)
admin.site.register(DTContact)


@admin.register(DeveloperAPIKey)
class DeveloperAPIKeyAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "plan", "is_active", "prefix", "created_at")
    list_filter = ("plan", "is_active")
    search_fields = ("name", "owner__username", "prefix")
    readonly_fields = ("prefix", "key_hash", "created_at")
