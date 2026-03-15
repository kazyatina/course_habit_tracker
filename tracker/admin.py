from django.contrib import admin

from tracker.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """Административный интерфейс для управления привычками."""

    list_display = ("id", "creator", "place", "periodicity")
    list_filter = ("creator", "place")
    search_fields = ("creator", "place", "reward", "action")
