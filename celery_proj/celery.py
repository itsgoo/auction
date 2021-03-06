from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab




# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_proj.settings')

app = Celery('celery_proj')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()




app.conf.beat_schedule = {
    'update_post_status': {
    'task': 'celery_app.tasks.update_post_status',
    'schedule': crontab(hour="*", minute="0"),
    },
    'update_auctions_with_no_bids_status': {
    'task': 'celery_app.tasks.update_auctions_with_no_bids_status',
    'schedule': crontab(hour="*", minute="1"),
    },
    'everyDaySchedule': {
    'task': 'celery_app.tasks.everyDaySchedule',
    'schedule': crontab(hour="*", minute="2"),
    },
    'start_auction_notification': {
    'task': 'celery_app.tasks.start_auction_notification',
    'schedule': crontab(hour="*", minute="30,50"),
    },
}
# crontab(minute=0, hour=0)
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


