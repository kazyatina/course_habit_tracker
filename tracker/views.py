from rest_framework import generics, permissions

from .models import Habit
from .paginators import HabitPagination
from .permissions import IsOwnerOrReadOnlyPublic
from .serializers import HabitSerializer


class HabitListAPIView(generics.ListAPIView):
    """Список привычек текущего пользователя с пагинацией."""

    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = HabitPagination

    def get_queryset(self):
        user = self.request.user
        return Habit.objects.filter(creator=user)


class PublicHabitListAPIView(generics.ListAPIView):
    """Список публичных привычек."""

    serializer_class = HabitSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = HabitPagination

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)


class HabitCreateAPIView(generics.CreateAPIView):
    """Создание привычки."""

    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class HabitRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Редактирование и удаление привычки."""

    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnlyPublic]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Habit.objects.all()
        user = self.request.user
        return Habit.objects.filter(creator=user) | Habit.objects.filter(is_public=True)
