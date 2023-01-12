import os

from celery import Celery
from celery.schedules import crontab
from .settings import TIME_ZONE

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dbShop.settings')

app = Celery('messageSenderService')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.timezone = TIME_ZONE
app.conf.beat_schedule = {
    'create-working-day': {
        'task': 'shopAuth.tasks.create_working_day',
        'schedule': crontab(minute=0, hour=0)
    },
    'add-day-off': {
        'task': 'shopAuth.tasks.add_day_off',
        'schedule': crontab(minute=0, hour=0)
    },
    'notify-about-end-working-day': {
        'task': 'notify_about_end_work_day',
        'schedule': crontab(minute=0, hour=0)  # додумать
    },
    'close_work_day': {
        'task': 'shopAuth.tasks.add_day_off',
        'schedule': crontab(minute=5, hour=0)
    },
    'start-inventory': {
        'task': 'shop.tasks.start_inventory',
        'schedule': crontab(minute=0, hour=0)
    },
}
