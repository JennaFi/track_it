import json

import requests
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django_celery_beat.models import PeriodicTask, ClockedSchedule

from config.settings import BOT_TOKEN, TELEGRAM_URL
from habits.models import Habit


def send_telegram_message(chat_id, message):
    """Send a telegram message"""
    params = {
        'text': message,
        'chat_id': chat_id,
    }

    requests.get(f"{TELEGRAM_URL}{BOT_TOKEN}/sendMessage", params=params)


@receiver(post_save, sender=Habit)
def schedule_habit_reminder(sender, instance, created, **kwargs):
    """Planning a task"""
    task_name = f"Habit reminder for habit {instance.pk}"

    if not created:
        try:
            task = PeriodicTask.objects.get(name=task_name)
            task.delete()
        except PeriodicTask.DoesNotExist:
            pass

    now = timezone.now()
    habit_time = timezone.datetime.combine(now.date(), instance.time)

    if timezone.is_naive(habit_time):
        habit_time = timezone.make_aware(habit_time)

    if habit_time < now:
        habit_time += timezone.timedelta(days=instance.periodicity)

    clocked_schedule, _ = ClockedSchedule.objects.get_or_create(clocked_time=habit_time)

    PeriodicTask.objects.create(clocked=clocked_schedule, name=task_name, task='habits.tasks.send_habit_reminder',
                                args=json.dumps([instance.pk]),
                                one_off=True,
                                )


@receiver(post_delete, sender=Habit)
def delete_habit_reminders(sender, instance, **kwargs):
    """Delete all tasks associated with a Habit"""

    tasks = PeriodicTask.objects.filter(
        name__startswith=f"Habit reminder for habit {instance.pk}"
    )
    tasks.delete()
