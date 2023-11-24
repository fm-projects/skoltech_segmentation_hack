from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "added")
    list_filter = ("status", "added")
    search_fields = ("id",)
    readonly_fields = ("id", "added", "status")
    fieldsets = (
        ("Primary", {"fields": ("id", "status", "added")}),
        ("Images", {"fields": ("original_image", "processed_image")}),
    )
