from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.prod')

app = Celery('config')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('settings.prod', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
#
#
# app.conf.beat_schedule = {
#     'delete-finished_games-every-day': {
#         'task': 'app.game.tasks.delete_finished_games',
#         'schedule': crontab(hour=0, minute=0),
#     },
# }
