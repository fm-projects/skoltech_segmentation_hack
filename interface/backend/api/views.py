from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework import mixins
from .models import Task, TaskSerializer, TaskCreateSerializer
from .tasks import process_task


class TaskViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """Create, retrieve and list tasks."""

    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return TaskCreateSerializer
        return TaskSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = TaskSerializer(self.perform_create(serializer)).data
        return Response(data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        task = serializer.save()
        process_task.delay(task.id)
        return task
