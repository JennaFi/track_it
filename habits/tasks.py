import json

from celery import shared_task
from django.utils import timezone
from django_celery_beat.clockedschedule import clocked
from django_celery_beat.models import ClockedSchedule, PeriodicTask

from .models import Habit
from .services import send_telegram_message


@shared_task
def send_habit_reminder(habit_id):
    """Send a reminder and creating a new task"""
    habit = Habit.objects.get(id=habit_id)

    if habit.user and habit.user.tg_chat_id:
        message = (
            f"Reminder: {habit.action} in {habit.location} at{habit.time.strftime('%H:%M')}.\n"
            f"You can get a prize: {habit.award}!"
        )
        send_telegram_message(habit.user.tg_chat_id, message)

    now = timezone.now()
    next_action_time = timezone.datetime.combine(
        now.date() + timezone.timedelta(days=habit.frequency), habit.time().strftime('%H:%M')
    )

    if timezone.is_naive(next_action_time):
        next_action_time = timezone.make_aware(next_action_time)

    if next_action_time < now:
        next_action_time += timezone.timedelta(days=habit.frequency)

    clocked_schedule, _ = ClockedSchedule.objects.get_or_create(clocked_time=next_action_time)

    PeriodicTask.objects.get_or_create(clocked=clocked_schedule,
                                       name=f"Habit reminder for habit {habit.pk} - {next_action_time}",
                                       task='habits.tasks.send_habit_reminder',
                                       args=json.dumps([habit.pk]),
                                       one_off=True,
                                       )
