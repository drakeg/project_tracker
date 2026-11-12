from django.contrib import admin

from .models import (
    Alignment,
    Comment,
    Contact,
    DeveloperAPIKey,
    DTContact,
    Keyword,
    MaturityModel,
    Status,
    Task,
    Tracker,
    Update,
)


@admin.register(Tracker)
class TrackerAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "status",
        "task",
        "contact",
        "dtcontact",
        "start_date",
        "end_date",
        "create_date",
    )
    list_filter = ("status", "task", "alignment", "maturitymodel")
    search_fields = (
        "title",
        "contact__contact_fname",
        "contact__contact_lname",
        "dtcontact__dtcontact_fname",
        "dtcontact__dtcontact_lname",
        "keywords__keyword_text",
    )
    date_hierarchy = "create_date"
    filter_horizontal = ("keywords",)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "contact_lname",
        "contact_fname",
        "contact_username",
        "contact_email",
        "contact_phone",
    )
    search_fields = (
        "contact_fname",
        "contact_lname",
        "contact_username",
        "contact_email",
        "contact_phone",
    )


@admin.register(DTContact)
class DTContactAdmin(admin.ModelAdmin):
    list_display = ("dtcontact_lname", "dtcontact_fname", "dtcontact_phone")
    search_fields = ("dtcontact_fname", "dtcontact_lname", "dtcontact_phone")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("comment_date", "comment_user", "comment_tracker", "comment_text")
    list_filter = ("comment_date",)
    search_fields = (
        "comment_text",
        "comment_user__contact_fname",
        "comment_user__contact_lname",
        "comment_tracker__title",
    )
    date_hierarchy = "comment_date"


@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = ("update_date", "update_user", "update_tracker", "update_text")
    list_filter = ("update_date",)
    search_fields = (
        "update_text",
        "update_user__contact_fname",
        "update_user__contact_lname",
        "update_tracker__title",
    )
    date_hierarchy = "update_date"


admin.site.register(Task)
admin.site.register(Status)
admin.site.register(Keyword)
admin.site.register(Alignment)
admin.site.register(MaturityModel)


@admin.register(DeveloperAPIKey)
class DeveloperAPIKeyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
        "plan",
        "is_active",
        "prefix",
        "last_used_at",
        "created_at",
    )
    list_filter = ("plan", "is_active")
    search_fields = ("name", "owner__username", "prefix")
    readonly_fields = ("prefix", "key_hash", "last_used_at", "created_at")
