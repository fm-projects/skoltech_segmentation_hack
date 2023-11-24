from django.db import models
from rest_framework import serializers


class Task(models.Model):
    class Status(models.IntegerChoices):
        QUEUED = 0
        PROCESSING = 1
        DONE = 2
        ERROR = 3

    original_image = models.ImageField(upload_to="originals")
    processed_image = models.ImageField(upload_to="processed", blank=True)
    status = models.IntegerField(choices=Status.choices, default=Status.QUEUED)
    added = models.DateTimeField(auto_now_add=True, verbose_name="Created")

    class Meta:
        ordering = ["-added"]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ["id", "added", "status", "processed_image"]


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["original_image"]
