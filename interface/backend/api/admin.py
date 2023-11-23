from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "added")
    list_filter = ("status", "added")
    search_fields = ("id",)
    readonly_fields = ("id", "added")
    fieldsets = (
        ("Основное", {"fields": ("id", "status", "added")}),
        ("Изображения", {"fields": ("original_image", "processed_image")}),
    )
