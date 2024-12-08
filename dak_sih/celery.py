from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dak_sih.settings')

from django.conf import settings

app = Celery('dak_sih')  
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_connection_retry_on_startup = True

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print(f"[CELERY REQUEST] {self.request!r}")