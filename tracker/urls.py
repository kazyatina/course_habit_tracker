from django.urls import path

from tracker.apps import TrackerConfig

from .views import (
    HabitCreateAPIView,
    HabitListAPIView,
    HabitRetrieveUpdateDestroyAPIView,
    PublicHabitListAPIView,
)

app_name = TrackerConfig.name

urlpatterns = [
    path("habits/", HabitListAPIView.as_view(), name="habit_list"),
    path("habits/public/", PublicHabitListAPIView.as_view(), name="habit_public_list"),
    path("habits/create/", HabitCreateAPIView.as_view(), name="habit_create"),
    path(
        "habits/<int:pk>/",
        HabitRetrieveUpdateDestroyAPIView.as_view(),
        name="habit_detail",
    ),
]
