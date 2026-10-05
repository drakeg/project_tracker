from django.contrib import admin

from .models import (
    Alignment,
    Comment,
    Contact,
    DTContact,
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
