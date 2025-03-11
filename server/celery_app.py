# type: ignore

import os
import sys

from celery import Celery

sys.path.append(os.getcwd())
from config import settings

app = Celery("tasks", broker=settings.CELERY_QUEUE_URL)

app.autodiscover_tasks(["pin_sphere.content"], related_name="tasks")


if __name__ == "__main__":
    app.start()
