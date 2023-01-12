from datetime import date, timedelta
import pytz

from dbShop.celery import app
from .models import *


@app.task
def get_price_list_from_csv():
    """Тут делаем логику вытягивания из csv документа ценников и передачи их директору?"""
    pass


@app.task
def create_working_day():
    for user in CustomUser.objects.all():
        WorkingDay.objects.create(
            user=user
        )


@app.task
def add_day_off():
    for day in WorkingDay.objects.filter(
        today=(date.today() - timedelta(days=1)),
        start_day__isnull=True
    ):
        DayOff.objects.create(
            user=day.user,
            date=day.today
        )


@app.task
def notify_about_end_work_day():
    for day in WorkingDay.objects.filter(
        today=(date.today() - timedelta(days=1)),
        end_day__isnull=True,
        start_day__isnull=False
    ):
        Notification.objects.create(
            user=day.user,
            text="Подтвердите продолжение работы в течение 5 минут"
        )
        # тут логика с вебсокетами


@app.task
def close_work_day():
    for day in WorkingDay.objects.filter(
        today=(date.today() - timedelta(days=1)),
        end_day__isnull=True,
        start_day__isnull=False
    ):
        notify = Notification.objects.get(user=day.user, confirmed=False)
        if notify:
            notify.confirmed = True
            notify.save(update_fields=['confirmed'])
        day.end_day = day.user.job.start_work_day + timedelta(hours=day.user.job.production_hours)
        day.save(update_fields=['end_day'])
