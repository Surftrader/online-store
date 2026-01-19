import os
from celery import Celery

# Celery default settings module for 'shop' project.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')

app = Celery('shop')

# Read configuration from Django settings, using prefix 'CELERY_'.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks (tasks.py) from all registered Django app configs.
app.autodiscover_tasks()
