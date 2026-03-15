from celery import shared_task
from django.utils import timezone

from .models import Habit
from .services import parse_habit_time, send_telegram_message


@shared_task
def send_habit_reminders():
    """Напоминания о том, в какое время какие привычки необходимо выполнять."""

    now_utc = timezone.now()
    now_local = timezone.localtime(now_utc)
    current_time = now_local.time()
    current_hour_minute = current_time.strftime("%H:%M")

    habits = Habit.objects.all()

    for habit in habits:
        habit_time_str = habit.time
        habit_time_obj = parse_habit_time(habit_time_str)
        habit_hour_minute = habit_time_obj.strftime("%H:%M")

        if habit_hour_minute == current_hour_minute:
            chat_id = habit.creator.chat_id

            if not chat_id:
                continue

            message = f"Напоминание: пора выполнять привычку '{habit.action}'!"
            if habit.reward:
                message.append(f"🏆 <b>Твоя награда:</b> {habit.reward.name}")
            elif habit.linked_habit:
                message.append(
                    f"🏆 <b>Твоя связанная привычка:</b> {habit.linked_habit}. Выполняется после полезной привычки."
                )

            try:
                send_telegram_message(chat_id, message)
            except Exception as e:
                return e
