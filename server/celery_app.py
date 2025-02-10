# type: ignore

from celery import Celery
import sys
import os

sys.path.append(os.getcwd())
app = Celery("tasks", broker="amqp://pin_sphere:pin_sphere_prod@localhost:5672/")

app.autodiscover_tasks(["pin_sphere.images"], related_name="tasks")


if __name__ == "__main__":
    app.start()
