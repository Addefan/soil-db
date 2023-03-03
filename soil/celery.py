import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soil.settings")

app = Celery("soil")
app.config_from_object("django.conf:settings", namespace="CELERY")
