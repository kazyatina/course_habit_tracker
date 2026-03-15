import datetime

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import Habit

User = get_user_model()


class HabitAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1", email="user1@mail.com", password="123456"
        )
        self.user2 = User.objects.create_user(
            username="user2", email="user2@mail.com", password="123456"
        )

        self.client1 = APIClient()
        self.client1.force_authenticate(user=self.user1)

        self.client2 = APIClient()
        self.client2.force_authenticate(user=self.user2)

        self.client_anon = APIClient()

        self.habit1 = Habit.objects.create(
            creator=self.user1,
            action="Действие 1",
            time=datetime.time(7, 0),
            place="Улица",
            is_pleasant=True,
            periodicity=1,
            time_to_complete=10,
            reward="Награда 1",
            is_public=False,
        )
        self.habit2 = Habit.objects.create(
            creator=self.user2,
            action="Действие 2",
            time=datetime.time(12, 0),
            place="Работа",
            is_pleasant=False,
            periodicity=2,
            time_to_complete=20,
            reward="Награда 2",
            is_public=True,
        )

    def test_list_habits_current_user(self):
        url = reverse("tracker:habit_list")
        response = self.client1.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["action"], self.habit1.action)

    def test_list_public_habits(self):
        url = reverse("tracker:habit_public_list")
        response = self.client_anon.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        public_actions = [h["action"] for h in response.data["results"]]
        self.assertIn(self.habit2.action, public_actions)

    def test_create_habit_authenticated(self):
        url = reverse("tracker:habit_create")
        data = {
            "action": "Создать действие",
            "time": "07:00:00",
            "place": "Спортплощадка",
            "is_pleasant": True,
            "periodicity": 3,
            "time_to_complete": 30,
            "reward": "",
            "is_public": False,
        }
        response = self.client1.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["creator"], self.user1.email)
        self.assertEqual(response.data["action"], data["action"])

    def test_create_habit_unauthenticated(self):
        url = reverse("tracker:habit_create")
        data = {
            "action": "Неуспешное создание",
            "time": "07:00:00",
            "place": "Спортплощадка",
            "is_pleasant": True,
            "periodicity": 1,
            "time_to_complete": 15,
            "reward": "Конфета",
            "is_public": True,
        }
        response = self.client_anon.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_habit_owner(self):
        url = reverse("tracker:habit_detail", args=[self.habit1.pk])
        response = self.client1.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["action"], self.habit1.action)

    def test_retrieve_habit_not_owner_but_public(self):
        url = reverse("tracker:habit_detail", args=[self.habit2.pk])
        response = self.client1.get(
            url
        )  # user1 пытается получить публичную habit2 другого пользователя
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["action"], self.habit2.action)

    def test_retrieve_habit_not_owner_and_not_public(self):
        url = reverse("tracker:habit_detail", args=[self.habit1.pk])
        response = self.client2.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_habit_owner(self):
        url = reverse("tracker:habit_detail", args=[self.habit1.pk])
        data = {"action": "Обновленное действие"}
        response = self.client1.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit1.refresh_from_db()
        self.assertEqual(self.habit1.action, data["action"])

    def test_update_habit_not_owner(self):
        url = reverse("tracker:habit_detail", args=[self.habit1.pk])
        data = {"action": "Неудачное обновление"}
        response = self.client2.patch(url, data, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND
        )  # нет доступа к чужой привычке

    def test_delete_habit_owner(self):
        url = reverse("tracker:habit_detail", args=[self.habit1.pk])
        response = self.client1.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(pk=self.habit1.pk).exists())

    def test_delete_habit_not_owner(self):
        url = reverse("tracker:habit_detail", args=[self.habit1.pk])
        response = self.client2.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Habit.objects.filter(pk=self.habit1.pk).exists())

    def test_pagination_on_habit_list(self):
        for i in range(6):
            Habit.objects.create(
                creator=self.user1,
                action=f"Дополнительное действие {i}",
                time=datetime.time(12, 0),
                place="Город",
                is_pleasant=True,
                periodicity=1,
                time_to_complete=10,
                reward="Награда",
                is_public=False,
            )

        url = reverse("tracker:habit_list") + "?page=1"
        response = self.client1.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 5)

        url = reverse("tracker:habit_list") + "?page=1&page_size=5"
        response = self.client1.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 5)
        self.assertIn("next", response.data)
        self.assertIn("count", response.data)
