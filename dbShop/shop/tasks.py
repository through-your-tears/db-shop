from datetime import date, timedelta
import pytz

from dbShop.celery import app
from .models import *
from shopAuth.models import Notification, CustomUser, Role


@app.task
def start_inventory():
    Inventory.objects.create()
    Notification.objects.create(
        user=CustomUser.objects.get(role=Role.objects.get('director')),
        text='Сегодня началась инвентаризация',
    )
    for user in CustomUser.objects.filter(role=Role.objects.get('storekeeper')):
        Notification.objects.create(
            user=user,
            text='Сегодня началась инвентаризация',
        )
