from __future__ import absolute_import, unicode_literals
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.prod')
django.setup()

from celery import Celery
app = Celery('config')
app.config_from_object('settings.prod', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
