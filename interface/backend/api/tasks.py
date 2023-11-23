from ..celery import celery_app
from .models import Task
import time


@celery_app.task(bind=True)
def process_task(self, task_id):
    task = Task.objects.get(id=task_id)
    task.status = Task.Status.PROCESSING
    task.save()

    try:
        # Emulate ML model processing the image
        time.sleep(10)
        task.processed_image = task.original_image
        task.status = Task.Status.DONE
        task.save()
    except Exception as e:
        task.status = Task.Status.ERROR
        task.save()
        raise e
