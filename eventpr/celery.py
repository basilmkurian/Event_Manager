
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventpr.settings')

app = Celery('eventpr')

# Using a string here means the worker doesn’t have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send-event-reminders-every-hour': {
        'task': 'events.tasks.send_event_reminders',
        'schedule': 3600.0,  # Every hour
    },
}

app.conf.timezone = 'UTC'
